import { all, fork } from "redux-saga/effects";
import AnalyticSaga from "./analytics/saga";
import AuthSaga from "./auth/saga";

export default function* rootSaga() {
  yield all([fork(AuthSaga), fork(AnalyticSaga)]);
}
