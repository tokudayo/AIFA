export interface Analytic {
  id: number;
  userId: number;
  startTime: Date;
  endTime: Date;
  exercise: string;
  platform: string;
  count: object;
  correct?: string;
  createdAt: Date;
  updatedAt: Date;
}
