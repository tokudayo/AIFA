import { Analytic } from "../../types/analytic";
import {
  GET_ANALYTICS,
  GET_ANALYTICS_SUCCESS,
  GET_ANALYTICS_FAILED,
  GetAnalyticsAction,
  GetAnalyticsSuccessAction,
  GetAnalyticsFailedAction,
} from "./actionTypes";

export const getAnalytics = (): GetAnalyticsAction => {
  return {
    type: GET_ANALYTICS,
  };
};

export const getAnalyticsSuccess = (
  analytics: Analytic[]
): GetAnalyticsSuccessAction => {
  return {
    type: GET_ANALYTICS_SUCCESS,
    analytics,
  };
};

export const getAnalyticsFailed = (error: Error): GetAnalyticsFailedAction => {
  return {
    type: GET_ANALYTICS_FAILED,
    error,
  };
};
