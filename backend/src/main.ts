import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe());
  app.enableCors();

  //Swagger
  const swagConfig = new DocumentBuilder()
    .addBearerAuth()
    .setTitle('Capstone' + ' API')
    .setDescription('Capstone' + ' Backend API')
    .setVersion('1.0')
    .addTag('Capstone')
    .build();

  const document = SwaggerModule.createDocument(app, swagConfig);
  SwaggerModule.setup('/docs', app, document, {
    customSiteTitle: 'Capstone',
  });

  await app.listen(process.env.PORT || 3000);
}
bootstrap();
