import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): string {
    return 'Hello World!';
  }

  async test(image: Buffer): Promise<void> {
    console.log(image, 'Line #11 app.service.ts');
  }
}
