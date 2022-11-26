export class CreateAnalyticDto {
  userId: number;
  startTime: Date;
  endTime: Date;
  exercise: string;
  platform: string;
  count: object;
}
