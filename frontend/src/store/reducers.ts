import { combineReducers } from "redux";

import AuthReducer, { AuthState } from "./auth/reducer";
import AnalyticReducer, { AnalyticState } from "./analytics/reducer";

const rootReducer = combineReducers({
  AuthReducer,
  AnalyticReducer,
});

export default rootReducer;
export type RootState = {
  AuthReducer: AuthState;
  AnalyticReducer: AnalyticState;
};
