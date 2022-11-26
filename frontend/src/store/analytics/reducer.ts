import { Analytic } from "../../types/analytic";
import {
  GET_ANALYTICS_SUCCESS,
  GET_ANALYTICS_FAILED,
  AnalyticsAction,
  GET_ANALYTICS,
} from "./actionTypes";

export interface AnalyticState {
  analytics: Analytic[] | null;
  loading: boolean;
  error: {
    message: string;
  };
}

const initialState: AnalyticState = {
  analytics: null,
  loading: false,
  error: {
    message: "",
  },
};

export default function AnalyticReducer(
  state: AnalyticState = initialState,
  action: AnalyticsAction
): AnalyticState {
  switch (action.type) {
    case GET_ANALYTICS:
      state = {
        ...state,
        loading: true,
      };
      break;
    case GET_ANALYTICS_SUCCESS:
      state = {
        ...state,
        analytics: action.analytics,
        loading: false,
      };
      break;
    case GET_ANALYTICS_FAILED:
      state = {
        ...state,
        error: {
          message: action.error.message,
        },
        loading: false,
      };
      break;
  }
  return state;
}
