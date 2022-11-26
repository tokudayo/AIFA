export interface Analytic {
  id: number;
  userId: number;
  startTime: Date;
  endTime: Date;
  exercise: string;
  platform: string;
  count: object;
  createdAt: Date;
  updatedAt: Date;
}
