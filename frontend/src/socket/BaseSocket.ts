// @ts-ignore
import io from "socket.io-client";
import eventBus from "../event/event-bus";
import { SocketEvent } from "./SocketEvent";

export class BaseSocket {
  private static instance: BaseSocket;
  // @ts-ignore
  private socket;

  public static getInstance(): BaseSocket {
    if (!BaseSocket.instance) {
      BaseSocket.instance = new BaseSocket();
    }

    return BaseSocket.instance;
  }

  public connect(): void {
    this.socket = io(process.env.REACT_APP_WS_HOST as string, {
      transports: ["websocket"],
    });
    this.socket.on("alert", (data: any) => {
      eventBus.dispatch(SocketEvent.ALERT, data);
    });
  }

  public reconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
    }
    this.connect();
  }

  public joinUserRoom(userId: number, exercise: string) {
    this.socket.emit("join", `user,${userId},${exercise},web`)
  }

  emitLandmarkCamera(data: any): void {
    this.socket.emit("landmark_camera", data);
  }

  emitImageCamera(data: any): void {
    if (process.env.REACT_APP_SAMPLE === "true") {
      this.socket.emit("image_camera", data);
    }
  }

  emitLandmarkWebcam(data: any): void {
    this.socket.emit("landmark_webcam", data);
  }

  emitImageWebcam(data: any): void {
    if (process.env.REACT_APP_SAMPLE === "true") {
      this.socket.emit("image_webcam", data);
    }
  }

  joinCameraRoom(): void {
    this.socket.emit("join", "camera");
    this.socket.on("image", (data: any) => {
      eventBus.dispatch(SocketEvent.RECEIVED_IMAGE, data);
    });
  }

  leaveCameraRoom(): void {
    this.socket.emit("leave", "camera");
    this.socket.off("image");
  }

  public leaveUserRoom(userId: number) {
    this.socket.emit("leave", `user,${userId}`)
  }

  disconnectSocket(): void {
    if (this.socket) {
      this.socket.disconnect();
      return;
    }
  }
}
