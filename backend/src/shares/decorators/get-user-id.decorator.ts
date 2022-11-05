import {
  createParamDecorator,
  ExecutionContext,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import jwtDecode from 'jwt-decode';

interface PayloadJwt {
  sub: number;
  iat: number;
  exp: number;
}

export const UserID = createParamDecorator(
  (data: string, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    try {
      const token = request.headers.authorization;
      const payload: PayloadJwt = jwtDecode(token);
      return payload.sub;
    } catch (e) {
      throw new HttpException(
        { key: 'NOT_VALID_ACCESS_TOKEN' },
        HttpStatus.BAD_REQUEST,
      );
    }
  },
);
