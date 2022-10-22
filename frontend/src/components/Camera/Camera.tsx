import { drawConnectors, drawLandmarks } from "@mediapipe/drawing_utils";
import { Pose, POSE_CONNECTIONS } from "@mediapipe/pose";
import { Col, Row } from "antd";
import { useCallback, useEffect, useState } from "react";
import io from "socket.io-client";

const socket = io(process.env.REACT_APP_WS_HOST as string);

const CameraStreamCapture = () => {
  const [isStreaming, setIsStreaming] = useState(false);

  useEffect(() => {
    return () => {
      socket.off("connect");
    };
  }, []);

  const streamCamVideo = useCallback(() => {
    socket.emit("join", { room: "camera" });
    const canvasElement: any =
      document.getElementsByClassName("output_canvas")[0];
    const canvasCtx: any = canvasElement.getContext("2d");
    const inputCanvasElement: any =
      document.getElementsByClassName("input_canvas")[0];
    const inputCanvasCtx: any = inputCanvasElement.getContext("2d");

    function onResults(results: any) {
      if (!results.poseLandmarks) {
        canvasCtx.drawImage(
          results.image,
          0,
          0,
          canvasElement.width,
          canvasElement.height
        );
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
      if (results.poseLandmarks) {
        drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, {
          color: "#00FF00",
          lineWidth: 4,
        });
        drawLandmarks(canvasCtx, results.poseLandmarks, {
          color: "#FF0000",
          lineWidth: 2,
        });
        socket.emit("landmark_camera", { data: results.poseLandmarks, date: Date.now() });
      }
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

    let blob: Blob;

    socket.on("image", async function (arrayBuffer) {
      blob = new Blob([arrayBuffer]);
      const img = new Image();
      img.onload = () => {
        inputCanvasCtx.drawImage(
          img,
          0,
          0,
          inputCanvasElement.width,
          inputCanvasElement.height
        );
        inputCanvasElement.toBlob((blob: Blob) => {
          socket.emit("image_camera", { data: blob, date: Date.now() });
        });
        pose.send({ image: inputCanvasElement });
      };
      img.src = URL.createObjectURL(blob);
    });

    setIsStreaming(true);
  }, []);

  const stopStreaming = useCallback(() => {
    socket.emit("leave", { room: "camera" });
    setIsStreaming(false);
  }, []);

  return (
    <>
      <Row gutter={16} style={!isStreaming ? { display: "none" } : {}}>
        <Col span={12}>
          <canvas
            className="input_canvas"
            width="640px"
            height="360px"
          ></canvas>
        </Col>
        <Col span={12}>
          <canvas
            className="output_canvas"
            width="640px"
            height="360px"
          ></canvas>
        </Col>
      </Row>
      {!isStreaming && (
        <button onClick={streamCamVideo}>Start streaming</button>
      )}
      {isStreaming && <button onClick={stopStreaming}>Stop streaming</button>}
    </>
  );
};

export default CameraStreamCapture;
