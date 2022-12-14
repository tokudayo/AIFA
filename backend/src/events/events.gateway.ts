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
import { CreateAnalyticDto } from 'src/analytics/dto/create-analytic.dto';
import { AnalyticsService } from 'src/analytics/analytics.service';

type MapAnalyticsDto = {
  [clientId: string]: CreateAnalyticDto;
};
const datas: MapAnalyticsDto = {};
const sockets = {};

function getRoomPayload(client: Socket) {
  let roomRep = null;

  client.rooms.forEach((room) => {
    const id = getId(room);
    if (id) {
      roomRep = room;
    }
  });
  return roomRep;
}

function getId(room: string) {
  if (room.startsWith('user,')) {
    return Number(room.split(',')[1]);
  }
  return null;
}

function getExercise(room: string) {
  if (room.startsWith('user,')) {
    return room.split(',')[2];
  }
  return null;
}

function getPlatform(room: string) {
  if (room.startsWith('user,')) {
    return room.split(',')[3];
  }
  return null;
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

  constructor(private readonly analyticsService: AnalyticsService) {}

  async disconnect(clientId: string) {
    if (datas[clientId]) {
      datas[clientId].endTime = new Date();
      const data = JSON.parse(JSON.stringify(datas[clientId]));
      delete datas[clientId];
      await this.analyticsService.create(data);
    }
  }

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
    console.log('Room: ' + new Array(...client.rooms).join(' '));
    this.disconnect(client.id);
  }

  handleConnection(client: Socket) {
    console.log(`Client connected: ${client.id}`);
    client.on('join', (room: string) => {
      console.log(`Client join room: ${room}`);
      client.join(room);
      const userId = getId(room);
      const exercise = getExercise(room);
      const platform = getPlatform(room);
      if (userId) {
        sockets[userId] = client.id;
        datas[client.id] = {
          userId,
          startTime: new Date(),
          endTime: new Date(),
          count: {},
          exercise: exercise,
          platform,
        };
      }
    });
    client.on('leave', (room: string) => {
      const userId = getId(room);
      client.leave(room);
      if (userId) {
        this.disconnect(client.id);
      }
    });
  }

  async onModuleInit() {
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
        const userId = getId(res[0]);
        if (sockets[userId] && datas[sockets[userId]]) {
          const alert = res[1] == '' ? 'Correct' : res[1];
          if (!datas[sockets[userId]].count[alert]) {
            datas[sockets[userId]].count[alert] = 0;
          }
          ++datas[sockets[userId]].count[alert];
        }
      },
    });

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
      `rtspsrc location=${process.env.RTSP_URL} latency=50 ! queue ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! video/x-raw,framerate=${fps}/1 ! jpegenc ! appsink name=sink`,
    );
    const appsink = pipeline.findChild('sink');
    pipeline.play();
    appsink.pull(onPull.bind(null, this.server));
  }

  async onModuleDestroy() {
    await this.producer.disconnect();
    await this.consumer.disconnect();
  }
}
