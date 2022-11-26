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
import { Kafka } from 'kafkajs';

function getRoomPayload(client: Socket) {
  let roomRep = null;

  client.rooms.forEach((room) => {
    if (room.length === 36) {
      roomRep = room;
    }
  });
  return roomRep;
}

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
  private kafka = new Kafka({
    clientId: 'web',
    brokers: [process.env.KAFKA_URL],
  });
  private consumer = this.kafka.consumer({ groupId: 'process.payload.reply' });
  private producer = this.kafka.producer();

  async sendLandmark(client: Socket, data: any) {
    data.room = getRoomPayload(client);
    if (!data.room) {
      return;
    }

    this.producer.send({
      topic: 'process.payload',
      messages: [
        {
          value: JSON.stringify(data),
        },
      ],
    });
  }

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

    this.sendLandmark(client, {
      exercise: payload.exercise,
      data: payload.data,
      date,
      width: payload.width,
      height: payload.height,
    });

    if (process.env.SAMPLE == 'true')
      writeFile(
        `sample/camera/${date}_landmark.json`,
        JSON.stringify(payload.data),
      );
  }

  @SubscribeMessage('landmark_webcam')
  async handleLandmarkWebcam(client: Socket, payload: any): Promise<void> {
    const date = payload.date;

    this.sendLandmark(client, {
      exercise: payload.exercise,
      data: payload.data,
      date,
      width: payload.width,
      height: payload.height,
    });

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

    console.log(
      payload[2],
      payload[3],
      payload[4],
      'Line #126 events.gateway.ts',
    );

    this.sendLandmark(client, {
      exercise: payload[2],
      data: payload[0],
      date: payload[1],
      width: Number(payload[3]),
      height: Number(payload[4]),
    });

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
    client.on('join', (room: string) => {
      client.join(room);
    });
    client.on('leave', (room: string) => {
      client.leave(room);
    });
  }

  async onModuleInit() {
    const fps = 10;
    function onPull(socket, buf) {
      if (buf) {
        socket.to('camera').emit('image', buf);
        appsink.pull(onPull.bind(null, socket));
      } else {
        console.log('NULL BUFFER');
        setTimeout(() => appsink.pull(onPull.bind(null, socket)), 1000 / fps);
      }
    }

    const pipeline = new gstreamer.Pipeline(
      `rtspsrc location=${process.env.RTSP_URL} ! queue ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! video/x-raw,framerate=${fps}/1 ! jpegenc quality=50 ! appsink name=sink`,
    );
    const appsink = pipeline.findChild('sink');

    pipeline.play();
    appsink.pull(onPull.bind(null, this.server));

    // KAFKA
    await this.producer.connect();
    await this.consumer.connect();
    await this.consumer.subscribe({
      topic: 'process.payload.reply',
      fromBeginning: false,
    });
    await this.consumer.run({
      eachMessage: async ({ message }) => {
        const res = JSON.parse(message.value.toString());
        this.server.to(res[0]).emit('alert', res[1]);
      },
    });
  }

  async onModuleDestroy() {
    await this.producer.disconnect();
    await this.consumer.disconnect();
  }
}
