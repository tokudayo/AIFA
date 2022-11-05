import { HttpException, HttpStatus, Injectable } from '@nestjs/common';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { Response } from 'src/shares/interceptors/response.interceptor';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { UserEntity } from './entities/user.entity';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(UserEntity)
    private userRepository: Repository<UserEntity>,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<UserEntity> {
    return this.userRepository.save(createUserDto);
  }

  async findAll(
    pageNumber?: number,
    pageSize?: number,
  ): Promise<Response<UserEntity[]>> {
    const qb = this.userRepository.createQueryBuilder('users');

    if (pageSize && pageNumber) {
      qb.limit(pageSize).offset((pageNumber - 1) * pageSize);
    }

    const [rs, total] = await Promise.all([qb.getRawMany(), qb.getCount()]);
    return {
      data: rs,
      pageNumber: Number(pageNumber),
      pageSize: Number(pageSize),
      total: total,
    };
  }

  async findOne(id: number): Promise<UserEntity> {
    return this.userRepository
      .createQueryBuilder('users')
      .where('users.id = :id', { id })
      .getOne();
  }

  async update(id: number, updateUserDto: UpdateUserDto): Promise<UserEntity> {
    await this.userRepository.update(id, updateUserDto);
    return this.findOne(id);
  }

  async remove(id: number): Promise<void> {
    await this.userRepository.delete(id);
  }

  async setRefreshToken(refreshToken: string, userId: number): Promise<void> {
    await this.userRepository.update(userId, {
      refreshToken,
    });
  }

  async getUserIfRefreshTokenMatch(
    refreshToken: string,
    userId: number,
  ): Promise<UserEntity> {
    const user = await this.userRepository.findOne({
      select: ['id', 'refreshToken'],
      where: {
        id: userId,
      },
    });

    if (!user)
      throw new HttpException({ key: 'NOT_EXISTS' }, HttpStatus.NOT_FOUND);

    const isRefreshTokenMatching = user.refreshToken === refreshToken;

    if (!isRefreshTokenMatching)
      throw new HttpException(
        { key: 'REFRESH_TOKEN_INVALID' },
        HttpStatus.UNAUTHORIZED,
      );

    return user;
  }

  async findByEmail(email: string): Promise<UserEntity> {
    return this.userRepository
      .createQueryBuilder('users')
      .where('users.email ILIKE :email', { email: `%${email}%` })
      .getOne();
  }
}
