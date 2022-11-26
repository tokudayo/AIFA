import { Module } from '@nestjs/common';
import { AnalyticsModule } from 'src/analytics/analytics.module';
import { EventsGateway } from './events.gateway';

@Module({
  imports: [AnalyticsModule],
  providers: [EventsGateway],
})
export class EventsModule {}
