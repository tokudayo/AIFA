import { Controller, Get, Post } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { AppService } from './app.service';
import { UploadedFile, UseInterceptors } from '@nestjs/common/decorators';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @Post('upload')
  @UseInterceptors(FileInterceptor('image'))
  async test(@UploadedFile() file: Express.Multer.File): Promise<void> {
    return this.appService.test(file.buffer);
  }
}
