import { takeLatest, put, call } from "redux-saga/effects";
import { GET_ANALYTICS } from "./actionTypes";
import { getAnalyticsSuccess, getAnalyticsFailed } from "./actions";
import { Analytic } from "../../types/analytic";
import { axiosInstance } from "../../helpers/axios";
import { AxiosResponse } from "axios";
import StorageUtils from "../../helpers/storage";

function* onGetAnalytics() {
  try {
    const response: AxiosResponse<Analytic[]> = yield call(() =>
      axiosInstance.get("analytics", {
        headers: {
          Authorization: `Bearer ${StorageUtils.getToken()}`,
        },
      })
    );

    yield put(getAnalyticsSuccess(response.data));
  } catch (error) {
    if (error instanceof Error) yield put(getAnalyticsFailed(error));
  }
}

function* AnalyticSaga() {
  yield takeLatest(GET_ANALYTICS, onGetAnalytics);
}

export default AnalyticSaga;
