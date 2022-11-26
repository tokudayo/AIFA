import { Injectable } from '@nestjs/common';
import { CreateAnalyticDto } from './dto/create-analytic.dto';
import { Response } from 'src/shares/interceptors/response.interceptor';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { AnalyticEntity } from './entities/analytic.entity';

@Injectable()
export class AnalyticsService {
  constructor(
    @InjectRepository(AnalyticEntity)
    private analyticRepository: Repository<AnalyticEntity>,
  ) {}

  async create(createAnalyticDto: CreateAnalyticDto): Promise<AnalyticEntity> {
    return this.analyticRepository.save(createAnalyticDto);
  }

  async findAll(
    pageNumber?: number,
    pageSize?: number,
  ): Promise<Response<AnalyticEntity[]>> {
    const qb = this.analyticRepository.createQueryBuilder('analytics');

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

  async findOne(id: number): Promise<AnalyticEntity> {
    return this.analyticRepository
      .createQueryBuilder('analytics')
      .where('analytics.id = :id', { id })
      .getOne();
  }

  async remove(id: number): Promise<void> {
    await this.analyticRepository.delete(id);
  }

  async findByUserId(userId: number): Promise<AnalyticEntity> {
    return this.analyticRepository
      .createQueryBuilder('analytics')
      .where('analytics."userId" = :userId', { userId })
      .getOne();
  }
}
