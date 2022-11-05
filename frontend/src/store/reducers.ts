import { combineReducers } from "redux";

import AuthReducer, { AuthState } from "./auth/reducer";

const rootReducer = combineReducers({
  AuthReducer,
});

export default rootReducer;
export type RootState = {
  AuthReducer: AuthState;
};
