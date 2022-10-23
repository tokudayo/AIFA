// eslint-disable-next-line
const gstreamer = require('gstreamer-superficial');
import {
  SubscribeMessage,
  WebSocketGateway,
  OnGatewayInit,
  WebSocketServer,
  OnGatewayConnection,
  OnGatewayDisconnect,
} from '@nestjs/websockets';
import { writeFile } from 'fs/promises';
import { Socket, Server } from 'socket.io';

@WebSocketGateway({
  maxHttpBufferSize: 1e8,
  cors: {
    origin: '*',
  },
})
export class EventsGateway
  implements OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect
{
  @WebSocketServer() server: Server;

  @SubscribeMessage('image_camera')
  async handleImageCamera(client: Socket, payload: any): Promise<void> {
    const date = payload.date;
    if (process.env.SAMPLE == 'true')
      writeFile(`sample/camera/${date}_image.png`, payload.data);
  }

  @SubscribeMessage('image_webcam')
  async handleImageWebcam(client: Socket, payload: any): Promise<void> {
    const date = payload.date;
    if (process.env.SAMPLE == 'true')
      writeFile(`sample/webcam/${date}_image.png`, payload.data);
  }

  @SubscribeMessage('image_mobile')
  async handleImageMobile(client: Socket, payload: any): Promise<void> {
    if (process.env.SAMPLE == 'true')
      writeFile(`sample/mobile/${payload[1]}_image.png`, payload[0]);
  }

  @SubscribeMessage('landmark_camera')
  async handleLandmarkCamera(client: Socket, payload: any): Promise<void> {
    const date = payload.date;
    if (process.env.SAMPLE == 'true')
      writeFile(
        `sample/camera/${date}_landmark.json`,
        JSON.stringify(payload.data),
      );
  }

  @SubscribeMessage('landmark_webcam')
  async handleLandmarkWebcam(client: Socket, payload: any): Promise<void> {
    const date = payload.date;
    if (process.env.SAMPLE == 'true')
      writeFile(
        `sample/webcam/${date}_landmark.json`,
        JSON.stringify(payload.data),
      );
  }

  @SubscribeMessage('landmark_mobile')
  async handleLandmarkMobile(client: Socket, payload: any): Promise<void> {
    payload[0] = JSON.parse(payload[0]).map((val) => ({
      x: val[0],
      y: val[1],
      z: val[2],
      visibility: val[3],
    }));
    if (process.env.SAMPLE == 'true')
      writeFile(
        `sample/mobile/${payload[1]}_landmark.json`,
        JSON.stringify(payload[0]),
      );
  }

  afterInit() {
    console.log('Init');
  }

  handleDisconnect(client: Socket) {
    console.log(`Client disconnected: ${client.id}`);
  }

  handleConnection(client: Socket) {
    console.log(`Client connected: ${client.id}`);
    client.on('join', (data) => {
      client.join(`room ${data.room}`);
    });
    client.on('leave', (data) => {
      client.leave(`room ${data.room}`);
    });
  }

  async onModuleInit() {
    this.server.emit('message', JSON.stringify(['Untranslatable']));

    const room = 'camera';
    const fps = 10;
    function onPull(socket, buf) {
      if (buf) {
        socket.to(`room ${room}`).emit('image', buf);
        appsink.pull(onPull.bind(null, socket));
      } else {
        console.log('NULL BUFFER');
        setTimeout(() => appsink.pull(onPull.bind(null, socket)), 1000 / fps);
      }
    }

    const pipeline = new gstreamer.Pipeline(
      `rtspsrc location=rtsp://${process.env.RTSP_USER}:${process.env.RTSP_PASSWORD}@192.168.1.110:554/Streaming/Channels/101 latency=100 ! queue ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! video/x-raw,framerate=${fps}/1 ! pngenc ! appsink name=sink`,
    );
    const appsink = pipeline.findChild('sink');

    pipeline.play();
    appsink.pull(onPull.bind(null, this.server));
  }
}