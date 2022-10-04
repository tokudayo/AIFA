import { Camera } from "@mediapipe/camera_utils";
import { drawConnectors, drawLandmarks } from "@mediapipe/drawing_utils";
import { Pose, POSE_CONNECTIONS } from "@mediapipe/pose";
import { Col, Row } from "antd";
import { useCallback, useEffect, useState } from "react";
import io from "socket.io-client";

const socket = io("ws://localhost:13051");

const WebcamStreamCapture = () => {
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [isStreaming, setIsStreaming] = useState(false);

  useEffect(() => {
    socket.on("connect", () => {
      setIsConnected(true);
    });

    return () => {
      socket.off("connect");
    };
  }, []);

  const emitScoket = useCallback((blob: Blob) => {
    socket.emit("message", blob);
  }, []);

  const getFrame = useCallback(() => {
    const video: any = document.querySelector("video");
    const canvas: any = document.getElementById("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    canvas.toBlob(async (blob: Blob) => {
      emitScoket(blob);
    });
  }, [emitScoket]);

  const streamCamVideo = useCallback(() => {
    const videoElement: any = document.getElementsByClassName("input_video")[0];
    const canvasElement: any =
      document.getElementsByClassName("output_canvas")[0];
    const canvasCtx: any = canvasElement.getContext("2d");

    function onResults(results: any) {
      if (!results.poseLandmarks) {
        return;
      }

      canvasCtx.save();
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      canvasCtx.drawImage(
        results.segmentationMask,
        0,
        0,
        canvasElement.width,
        canvasElement.height
      );

      // Only overwrite existing pixels.
      canvasCtx.globalCompositeOperation = "source-in";
      canvasCtx.fillStyle = "rgba(255, 255, 255, 0)";
      canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);

      // Only overwrite missing pixels.
      canvasCtx.globalCompositeOperation = "destination-atop";
      canvasCtx.drawImage(
        results.image,
        0,
        0,
        canvasElement.width,
        canvasElement.height
      );

      canvasCtx.globalCompositeOperation = "source-over";
      drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, {
        color: "#00FF00",
        lineWidth: 4,
      });
      drawLandmarks(canvasCtx, results.poseLandmarks, {
        color: "#FF0000",
        lineWidth: 2,
      });
      canvasCtx.restore();
    }

    const pose = new Pose({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
      },
    });
    pose.setOptions({
      modelComplexity: 1,
      smoothLandmarks: true,
      enableSegmentation: true,
      smoothSegmentation: true,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });
    pose.onResults(onResults);

    const camera = new Camera(videoElement, {
      onFrame: async () => {
        await pose.send({ image: videoElement });
      },
      width: 640,
      height: 360,
    });
    camera.start();
    setIsStreaming(true);
  }, []);

  return (
    <>
      <body>
        <Row gutter={16} style={!isStreaming ? { display: "none" } : {}}>
          <Col span={12}>
            <video className="input_video"></video>
          </Col>
          <Col span={12}>
            <canvas
              className="output_canvas"
              width="640px"
              height="360px"
            ></canvas>
          </Col>
        </Row>
        <button onClick={streamCamVideo}>Start streaming</button>
      </body>
    </>
  );
};

export default WebcamStreamCapture;
