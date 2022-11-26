import { AnalyticEntity } from 'src/analytics/entities/analytic.entity';
import {
  Entity,
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
  Column,
  OneToMany,
} from 'typeorm';

@Entity('users')
export class UserEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  email: string;

  @Column({ nullable: true })
  refreshToken?: string;

  @Column({ nullable: true })
  password?: string;

  @OneToMany(() => AnalyticEntity, (analytic) => analytic.user)
  analytics: AnalyticEntity[];

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
