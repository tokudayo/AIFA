import { Analytic } from "../../types/analytic";

export const GET_ANALYTICS = "GET_ANALYTICS";
export interface GetAnalyticsAction {
  type: typeof GET_ANALYTICS;
}

export const GET_ANALYTICS_SUCCESS = "GET_ANALYTICS_SUCCESS";
export interface GetAnalyticsSuccessAction {
  type: typeof GET_ANALYTICS_SUCCESS;
  analytics: Analytic[];
}

export const GET_ANALYTICS_FAILED = "GET_ANALYTICS_FAILED";
export interface GetAnalyticsFailedAction {
  type: typeof GET_ANALYTICS_FAILED;
  error: Error;
}

export type AnalyticsAction =
  | GetAnalyticsAction
  | GetAnalyticsSuccessAction
  | GetAnalyticsFailedAction;
