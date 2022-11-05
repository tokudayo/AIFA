import { User } from "../../types/user";

export interface AuthRequest {
  email: string;
  password: string;
}

export interface SignUpRequest {
  email: string;
  password: string;
  passwordConfirmation: string;
}

export interface AuthResponse {
  user: User | null;
  accessToken: string;
  refreshToken: string;
}

export const SIGN_UP = "SIGN_UP";
export interface SignUpAction {
  type: typeof SIGN_UP;
  signUpRequest: SignUpRequest;
}

export const SIGN_UP_SUCCESS = "SIGN_UP_SUCCESS";
export interface SignUpSuccessAction {
  type: typeof SIGN_UP_SUCCESS;
}

export const SIGN_UP_FAIL = "SIGN_UP_FAIL";
export interface SignUpFailAction {
  type: typeof SIGN_UP_FAIL;
  error: unknown;
}

export const LOGIN = "LOGIN";
export interface LoginAction {
  type: typeof LOGIN;
  authRequest: AuthRequest;
}

export const LOGIN_SUCCESS = "LOGIN_SUCCESS";
export interface LoginSuccessAction {
  type: typeof LOGIN_SUCCESS;
  authResponse: AuthResponse;
}

export const LOGIN_FAIL = "LOGIN_FAIL";
export interface LoginFailAction {
  type: typeof LOGIN_FAIL;
  error: unknown;
}

export const LOGOUT = "LOGOUT";
export interface LogoutAction {
  type: typeof LOGOUT;
}

export const LOGOUT_SUCCESS = "LOGOUT_SUCCESS";
export interface LogoutSuccessAction {
  type: typeof LOGOUT_SUCCESS;
}

export const LOGOUT_FAIL = "LOGOUT_FAIL";
export interface LogoutFailAction {
  type: typeof LOGOUT_FAIL;
  error: unknown;
}

export const GET_LOGIN_STORAGE = "GET_LOGIN_STORAGE";
export interface GetLoginStorageAction {
  type: typeof GET_LOGIN_STORAGE;
}

export const CLEAR_ERROR = "CLEAR_ERROR";
export interface ClearErrorAction {
  type: typeof CLEAR_ERROR;
}

export const CLEAR_SIGN_UP_SUCCESS = "CLEAR_SIGN_UP_SUCCESS";
export interface ClearSignUpSuccessAction {
  type: typeof CLEAR_SIGN_UP_SUCCESS;
}

export type AuthAction =
  | SignUpAction
  | SignUpSuccessAction
  | SignUpFailAction
  | LoginAction
  | LoginSuccessAction
  | LoginFailAction
  | LogoutAction
  | GetLoginStorageAction
  | ClearErrorAction
  | LogoutSuccessAction
  | LogoutFailAction
  | ClearSignUpSuccessAction;
