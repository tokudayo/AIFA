import { Camera } from "@mediapipe/camera_utils";
import { drawConnectors, drawLandmarks } from "@mediapipe/drawing_utils";
import { Pose, POSE_CONNECTIONS } from "@mediapipe/pose";
import { Col, Row } from "antd";
import { useCallback, useState } from "react";
import { BaseSocket } from "../../socket/BaseSocket";

const WebcamStreamCapture = () => {
  const [isStreaming, setIsStreaming] = useState(false);
  const [camera, setCamera] = useState(undefined as any);

  const streamCamVideo = useCallback(() => {
    const videoElement: any = document.getElementsByClassName("input_video")[0];
    const canvasElement: any =
      document.getElementsByClassName("output_canvas")[0];
    const canvasCtx: any = canvasElement.getContext("2d");

    const hiddenCanvasElement: any =
      document.getElementsByClassName("hidden_canvas")[0];
    const hiddenCanvasCtx: any = hiddenCanvasElement.getContext("2d");

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
      hiddenCanvasCtx.drawImage(
        results.image,
        0,
        0,
        hiddenCanvasElement.width,
        hiddenCanvasElement.height
      );

      hiddenCanvasElement.toBlob((blob: Blob) => {
        BaseSocket.getInstance().emitImageWebcam({ data: blob, date: Date.now() });
      });
      
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
        BaseSocket.getInstance().emitLandmarkWebcam({ data: results.poseLandmarks, date: Date.now() });
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

    const cameraElem = new Camera(videoElement, {
      onFrame: async () => {
        await pose.send({ image: videoElement });
      },
      width: 640,
      height: 360,
    });
    cameraElem.start();
    setCamera(cameraElem);
    setIsStreaming(true);
  }, []);

  const stopStreaming = useCallback(() => {
    camera.stop();
    setIsStreaming(false);
  }, [camera]);

  return (
    <>
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
          <canvas
            className="hidden_canvas"
            width="640px"
            height="360px"
            hidden
          ></canvas>
        </Col>
      </Row>
      {!isStreaming && <button onClick={streamCamVideo}>Start streaming</button>}
      {isStreaming && <button onClick={stopStreaming}>Stop streaming</button>}
  </>
  );
};

export default WebcamStreamCapture;
