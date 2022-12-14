import { drawConnectors, drawLandmarks } from "@mediapipe/drawing_utils";
import { Pose, POSE_CONNECTIONS } from "@mediapipe/pose";
import { Button, Form, Row, Select } from "antd";
import { useCallback, useState } from "react";
import { useSelector } from "react-redux";
import eventBus from "../../event/event-bus";
import { BaseSocket } from "../../socket/BaseSocket";
import { SocketEvent } from "../../socket/SocketEvent";
import { RootState } from "../../store/reducers";

const CameraStreamCapture = () => {
  const [pose, setPose] = useState(undefined as any);
  const [isStreaming, setIsStreaming] = useState(false);
  const [form] = Form.useForm();
  const { user } = useSelector((state: RootState) => state.AuthReducer);

  const streamCamVideo = useCallback((exercise: string) => {
    BaseSocket.getInstance().joinCameraRoom();
    BaseSocket.getInstance().joinUserRoom(user?.id || 0, exercise);
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
        BaseSocket.getInstance().emitLandmarkWebcam({
          data: results.poseLandmarks,
          exercise: exercise,
          date: Date.now(),
          width: 1067,
          height: 600,
        });
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

    eventBus.on(SocketEvent.RECEIVED_IMAGE, async (arrayBuffer: any) => {
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
          BaseSocket.getInstance().emitImageCamera({
            data: blob,
            date: Date.now(),
          });
        });
        pose.send({ image: inputCanvasElement });
      };
      img.src = URL.createObjectURL(blob);
    });

    setPose(pose);
    setIsStreaming(true);
  }, [user]);

  const stopStreaming = useCallback(() => {
    BaseSocket.getInstance().leaveCameraRoom();
    BaseSocket.getInstance().leaveUserRoom(user?.id || 0);
    pose.close();
    setIsStreaming(false);
  }, [pose, user]);

  return (
    <Row gutter={16} justify="center" className={!isStreaming ? "mt-5" : ""}>
      <div style={!isStreaming ? { display: "none" } : {}}>
        <canvas
          className="input_canvas"
          width="1067px"
          height="600px"
          hidden
        ></canvas>
        <canvas
          className="output_canvas"
          width="1067px"
          height="600px"
        ></canvas>
      </div>
      {!isStreaming && (
        <Form
          className="mt-3"
          form={form}
          onFinish={(values) => {
            streamCamVideo(values.exercise);
          }}
        >
          <Form.Item name="exercise" initialValue="shoulder_press">
            <Select
              options={[
                {
                  value: "shoulder_press",
                  label: "Shoulder Press",
                },
                {
                  value: "deadlift",
                  label: "Deadlift",
                },
                {
                  value: "hammer_curl",
                  label: "Hammer Curl",
                },
              ]}
            />
          </Form.Item>
          <Button className="mt-5" type="primary" htmlType="submit">
            Start streaming
          </Button>
        </Form>
      )}
      {isStreaming && (
        <Button
          style={{ position: "absolute", bottom: "20px" }}
          danger
          onClick={stopStreaming}
        >
          Stop streaming
        </Button>
      )}
    </Row>
  );
};

export default CameraStreamCapture;
