import { UserEntity } from '../../users/entities/user.entity';

export class ResponseUserDto {
  accessToken: string;
  refreshToken: string;
  user: Partial<UserEntity>;
}
