import { ApiPropertyOptional } from '@nestjs/swagger';
import { Transform } from 'class-transformer';
import { IsInt, IsOptional, IsPositive, Max } from 'class-validator';

export class PaginationInput {
  @ApiPropertyOptional({ example: 1 })
  @Transform(({ value }) => Number(value))
  @IsInt()
  @IsPositive()
  @IsOptional()
  pageNumber?: number = 1;

  @ApiPropertyOptional({ example: 20 })
  @Transform(({ value }) => Number(value))
  @IsInt()
  @Max(10000)
  @IsPositive()
  @IsOptional()
  pageSize?: number = 20;
}
