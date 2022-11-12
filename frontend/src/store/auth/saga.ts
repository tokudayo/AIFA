import { takeLatest, put, call } from "redux-saga/effects";
import { GET_LOGIN_STORAGE, LOGIN, LOGOUT, SIGN_UP } from "./actionTypes";
import {
  loginSuccess,
  loginFail,
  login,
  signUp,
  signUpFail,
  signUpSuccess,
} from "./actions";
import { axiosInstance } from "../../helpers/axios";
import StorageUtils from "../../helpers/storage";
import { AxiosResponse } from "axios";
import { LoginResponse } from "../../types/response";

function saveLoginDataToStore({
  accessToken,
  refreshToken,
  user,
}: LoginResponse) {
  StorageUtils.setUser(user);
  StorageUtils.setToken(accessToken);
  StorageUtils.setRefreshToken(refreshToken);
}

function removeLoginDataFromStore() {
  StorageUtils.removeUser();
  StorageUtils.removeToken();
  StorageUtils.removeRefreshToken();
}

function* getLoginStorage() {
  const user = StorageUtils.getUser();
  const accessToken = StorageUtils.getToken();
  const refreshToken = StorageUtils.getRefreshToken();

  if (user && accessToken && refreshToken) {
    yield put(
      loginSuccess({
        user,
        accessToken,
        refreshToken,
      })
    );
  } else {
    yield put(
      loginSuccess({
        user: null,
        accessToken: "",
        refreshToken: "",
      })
    );
  }
}

function* onSignUp({ signUpRequest }: ReturnType<typeof signUp>) {
  try {
    yield call(() => axiosInstance.post("auth/sign-up", signUpRequest));
    yield put(signUpSuccess());
  } catch (error) {
    yield put(signUpFail(error));
  }
}

function* onLogin({ authRequest }: ReturnType<typeof login>) {
  try {
    const response: AxiosResponse<LoginResponse> = yield call(() =>
      axiosInstance.post("auth/login", {
        username: authRequest.email,
        password: authRequest.password,
      })
    );
    yield call(saveLoginDataToStore, response.data);
    yield call(getLoginStorage);
  } catch (error) {
    yield put(loginFail(error));
  }
}

function* onLogout() {
  try {
    yield call(removeLoginDataFromStore);
    yield call(getLoginStorage);
  } catch (error) {
    yield put(loginFail(error));
  }
}

function* AuthSaga() {
  yield takeLatest(LOGIN, onLogin);
  yield takeLatest(GET_LOGIN_STORAGE, getLoginStorage);
  yield takeLatest(LOGOUT, onLogout);
  yield takeLatest(SIGN_UP, onSignUp);
}

export default AuthSaga;
