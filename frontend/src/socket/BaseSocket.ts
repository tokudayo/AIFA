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
    console.log("cvboicuvb", "Line #20 BaseSocket.ts");

    this.socket = io(process.env.REACT_APP_WS_HOST as string, {
      transports: ["websocket"],
    });
  }

  public reconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
    }
    this.connect();
  }

  emitLandmarkCamera(data: any): void {
    this.socket.emit("landmark_camera", data);
  }

  emitImageCamera(data: any): void {
    this.socket.emit("image_camera", data);
  }

  emitLandmarkWebcam(data: any): void {
    this.socket.emit("landmark_webcam", data);
  }

  emitImageWebcam(data: any): void {
    this.socket.emit("image_webcam", data);
  }

  joinCameraRoom(): void {
    console.log("cvboiu", "Line #62 BaseSocket.ts");
    this.socket.emit("join", { room: "camera" });
    this.socket.on("image", (data: any) => {
      console.log("cvboiucvb", data, "Line #36 BaseSocket.ts");

      eventBus.dispatch(SocketEvent.RECIEVED_IMAGE, data);
    });
  }

  leaveCameraRoom(): void {
    this.socket.emit("leave", { room: "camera" });
    this.socket.off("image");
  }

  disconnectSocket(): void {
    if (this.socket) {
      this.socket.disconnect();
      return;
    }
  }
}
