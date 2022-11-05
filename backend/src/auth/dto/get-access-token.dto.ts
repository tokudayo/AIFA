import { IsNotEmpty } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class GetAccessTokenForm {
  @IsNotEmpty()
  @ApiProperty({
    required: true,
  })
  refreshToken: string;
}
