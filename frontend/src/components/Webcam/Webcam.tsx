import { Camera } from "@mediapipe/camera_utils";
import { drawConnectors, drawLandmarks } from "@mediapipe/drawing_utils";
import { Pose, POSE_CONNECTIONS } from "@mediapipe/pose";
import { Button, Row, Select, Form } from "antd";
import { useCallback, useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { BaseSocket } from "../../socket/BaseSocket";
import { RootState } from "../../store/reducers";

const WebcamStreamCapture = () => {
  const [isStreaming, setIsStreaming] = useState(false);
  const [camera, setCamera] = useState(undefined as any);
  const [pose, setPose] = useState(undefined as any);
  const [width, setWidth] = useState((680 * 16) / 9);
  const [height, setHeight] = useState(680);
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const [windowHeight, setWindowHeight] = useState(window.innerHeight);
  const [form] = Form.useForm();
  const { user } = useSelector((state: RootState) => state.AuthReducer);

  const streamCamVideo = useCallback(
    (exercise: string) => {
      BaseSocket.getInstance().joinUserRoom(user?.id || 0, exercise);
      const videoElement: any =
        document.getElementsByClassName("input_video")[0];
      const canvasElement: any =
        document.getElementsByClassName("output_canvas")[0];
      const canvasCtx: any = canvasElement.getContext("2d");

      function onResults(results: any) {
        canvasCtx.save();
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

        if (results.segmentationMask) {
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
          // canvasCtx.translate(canvasElement.width, 0);
          // canvasCtx.scale(-1, 1);
          canvasCtx.drawImage(
            results.image,
            0,
            0,
            canvasElement.width,
            canvasElement.height
          );
          canvasCtx.globalCompositeOperation = "source-over";
        } else {
          canvasCtx.drawImage(
            results.image,
            0,
            0,
            canvasElement.width,
            canvasElement.height
          );
        }

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
            width,
            height,
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
        selfieMode: true,
        modelComplexity: 1,
        smoothLandmarks: true,
        enableSegmentation: false,
        smoothSegmentation: true,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5,
      });
      pose.onResults(onResults);

      const cameraElem = new Camera(videoElement, {
        onFrame: async () => {
          await pose.send({ image: videoElement });
        },
        width: width,
        height: height,
      });
      cameraElem.start();
      setPose(pose);
      setCamera(cameraElem);
      setIsStreaming(true);
    },
    [width, height, user]
  );

  const stopStreaming = useCallback(() => {
    BaseSocket.getInstance().leaveUserRoom(user?.id || 0);
    camera.stop();
    pose.close();
    setIsStreaming(false);
  }, [camera, pose, user]);

  useEffect(() => {
    const video: any = document.getElementsByClassName("input_video")[0];
    (async () => {
      try {
        let constraints = { video: { width: 9999 } };
        video.srcObject = await navigator.mediaDevices.getUserMedia(
          constraints
        );
        let track = video.srcObject.getTracks()[0];
        let { width, height } = track.getSettings();
        setHeight(680);
        setWidth((width / height) * 680);
        console.log(`Resolution: ${width}x${height}`);
      } catch (e) {
        console.log(e);
      }
    })();
  }, []);

  useEffect(() => {
    const realRatio = width / height;
    const sideBarWidth = windowWidth > 1000 ? 200 : 50;
    const expectedRatio = (windowWidth - sideBarWidth) / windowHeight;
    const expectedWidth =
      windowWidth < 500
        ? (windowWidth * 11) / 10
        : ((windowWidth - sideBarWidth) * 96.5) / 100;
    const expectedHeight = (windowHeight * 96.5) / 100;

    if (realRatio < expectedRatio) {
      setHeight(expectedHeight);
      setWidth(expectedHeight * realRatio);
    } else {
      setWidth(expectedWidth);
      setHeight(expectedWidth / realRatio);
    }
  }, [windowWidth, windowHeight, width, height]);

  useEffect(() => {
    const updateWindowDimensions = () => {
      setWindowWidth(window.innerWidth);
      setWindowHeight(window.innerHeight);
    };

    window.addEventListener("resize", updateWindowDimensions);

    return () => window.removeEventListener("resize", updateWindowDimensions);
  }, []);

  return (
    <>
      <Row gutter={16} justify="center" className={!isStreaming ? "mt-5" : ""}>
        <div style={!isStreaming ? { display: "none" } : {}}>
          <video className="input_video" hidden></video>
          <canvas
            className="output_canvas"
            width={width}
            height={height}
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
    </>
  );
};

export default WebcamStreamCapture;
