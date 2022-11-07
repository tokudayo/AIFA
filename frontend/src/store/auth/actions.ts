import {
  CLEAR_ERROR,
  CLEAR_SIGN_UP_SUCCESS,
  SIGN_UP,
  SIGN_UP_SUCCESS,
  SIGN_UP_FAIL,
  LOGIN,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  GET_LOGIN_STORAGE,
  LOGOUT,
  SignUpRequest,
  AuthRequest,
  LoginAction,
  LoginSuccessAction,
  LoginFailAction,
  SignUpAction,
  SignUpSuccessAction,
  SignUpFailAction,
  LogoutAction,
  GetLoginStorageAction,
  ClearErrorAction,
  AuthResponse,
  LOGOUT_SUCCESS,
  LOGOUT_FAIL,
  LogoutSuccessAction,
  LogoutFailAction,
  ClearSignUpSuccessAction,
} from "./actionTypes";

export const signUp = (signUpRequest: SignUpRequest): SignUpAction => {
  return {
    type: SIGN_UP,
    signUpRequest,
  };
};

export const signUpSuccess = (): SignUpSuccessAction => {
  return {
    type: SIGN_UP_SUCCESS,
  };
};

export const signUpFail = (error: unknown): SignUpFailAction => {
  return {
    type: SIGN_UP_FAIL,
    error,
  };
};

export const login = (authRequest: AuthRequest): LoginAction => {
  return {
    type: LOGIN,
    authRequest,
  };
};

export const loginSuccess = (
  authResponse: AuthResponse
): LoginSuccessAction => {
  return {
    type: LOGIN_SUCCESS,
    authResponse,
  };
};

export const loginFail = (error: unknown): LoginFailAction => {
  return {
    type: LOGIN_FAIL,
    error,
  };
};

export const logout = (): LogoutAction => {
  return {
    type: LOGOUT,
  };
};

export const logoutSuccess = (): LogoutSuccessAction => {
  return {
    type: LOGOUT_SUCCESS,
  };
};

export const logoutFail = (error: unknown): LogoutFailAction => {
  return {
    type: LOGOUT_FAIL,
    error,
  };
};

export const getLoginStorage = (): GetLoginStorageAction => {
  return {
    type: GET_LOGIN_STORAGE,
  };
};

export const clearErrors = (): ClearErrorAction => {
  return {
    type: CLEAR_ERROR,
  };
};

export const clearSuccessSignUp = (): ClearSignUpSuccessAction => {
  return {
    type: CLEAR_SIGN_UP_SUCCESS,
  };
};
