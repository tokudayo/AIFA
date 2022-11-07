import { HttpException, HttpStatus, Injectable } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { ResponseUserDto } from './dto/response-user.dto';
import * as bcrypt from 'bcrypt';
import { UsersService } from '../users/users.service';
import { UserEntity } from '../users/entities/user.entity';

@Injectable()
export class AuthService {
  constructor(
    private userService: UsersService,
    private jwtService: JwtService,
  ) {}

  async validateUser(
    email: string,
    password: string,
  ): Promise<Partial<UserEntity>> {
    try {
      await this.checkPassword(email, password);
    } catch (err) {
      throw new HttpException(
        { key: 'WRONG_PASSWORD' },
        HttpStatus.BAD_REQUEST,
      );
    }

    return this.userService.findByEmail(email);
  }

  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  async login(req): Promise<ResponseUserDto> {
    const user = req.user;

    const payload = {
      sub: user.id,
      email: user.email,
    };
    const refreshTokenPayload = { sub: user.id };
    const refreshTokenConfig = {
      expiresIn: process.env.JWT_REFRESH_TOKEN_EXPIRATION_TIME,
      secret: process.env.JWT_REFRESH_TOKEN_SECRET,
    };
    const response = {
      accessToken: this.jwtService.sign(payload),
      refreshToken: this.jwtService.sign(
        refreshTokenPayload,
        refreshTokenConfig,
      ),
      user: {
        ...user,
      },
    };

    await this.userService.setRefreshToken(response.refreshToken, user.id);

    return response;
  }

  async signUp(
    email: string,
    password: string,
    passwordConfirmation: string,
  ): Promise<Partial<UserEntity>> {
    const existsUser = await this.userService.findByEmail(email);
    if (existsUser) {
      throw new HttpException(
        { key: 'USER_ALREDY_EXISTS' },
        HttpStatus.BAD_REQUEST,
      );
    }
    if (password != passwordConfirmation) {
      throw new HttpException(
        { key: 'PASSWORD_NOT_MATCH' },
        HttpStatus.BAD_REQUEST,
      );
    }
    const hashedPassword: string = await new Promise((resolve, reject) => {
      bcrypt.hash(password, 10, function (err: unknown, hash: string) {
        if (err) reject(err);
        resolve(hash);
      });
    });

    return this.userService.create({
      email,
      password: hashedPassword,
    });
  }

  async getAccessToken(refreshToken: string): Promise<{ accessToken: string }> {
    const refreshTokenConfig = {
      expiresIn: process.env.JWT_REFRESH_TOKEN_EXPIRATION_TIME,
      secret: process.env.JWT_REFRESH_TOKEN_SECRET,
    };
    let refreshTokenDecode;
    try {
      refreshTokenDecode = await this.jwtService.verify(
        refreshToken,
        refreshTokenConfig,
      );
    } catch (e) {
      throw new HttpException(
        { key: 'INVALID_TOKEN' },
        HttpStatus.UNAUTHORIZED,
      );
    }

    const userId = refreshTokenDecode.sub;
    const user = await this.userService.getUserIfRefreshTokenMatch(
      refreshToken,
      userId,
    );
    const payload = {
      sub: user.id,
      email: user.email,
    };

    return {
      accessToken: this.jwtService.sign(payload),
    };
  }

  async checkPassword(email: string, password: string) {
    const user = await this.userService.findByEmail(email);
    if (!this.comparePassword(password, user.password)) {
      throw new Error();
    }
  }

  private comparePassword(password: string, hashPassword: string) {
    return bcrypt.compareSync(password, hashPassword);
  }
}
