import { User } from "../../types/user";
import {
  SIGN_UP,
  SIGN_UP_SUCCESS,
  SIGN_UP_FAIL,
  LOGIN,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT,
  GET_LOGIN_STORAGE,
  CLEAR_ERROR,
  CLEAR_SIGN_UP_SUCCESS,
  AuthAction,
  LOGOUT_SUCCESS,
  LOGOUT_FAIL,
} from "./actionTypes";

export interface AuthState {
  user: User | null | undefined;
  accessToken: string;
  refreshToken: string;
  loading: boolean;
  signUpSuccess: boolean;
  error: {
    message: string;
  };
}

const initialState: AuthState = {
  user: undefined,
  accessToken: "",
  refreshToken: "",
  signUpSuccess: false,
  loading: false,
  error: {
    message: "",
  },
};

export default function AuthReducer(
  state: AuthState = initialState,
  action: AuthAction
): AuthState {
  switch (action.type) {
    case GET_LOGIN_STORAGE:
      state = { ...state };
      break;
    case SIGN_UP:
      state = { ...state, loading: true };
      break;
    case SIGN_UP_SUCCESS:
      state = {
        ...state,
        signUpSuccess: true,
        loading: false,
      };
      break;
    case SIGN_UP_FAIL:
      state = {
        ...state,
        error: {
          message: "Login Failed",
        },
        loading: false,
      };
      break;
    case LOGIN:
      state = { ...state, loading: true };
      break;
    case LOGIN_SUCCESS:
      state = {
        ...state,
        ...action.authResponse,
        loading: false,
      };
      break;
    case LOGIN_FAIL:
      state = {
        ...state,
        error: {
          message: "Login Failed",
        },
        loading: false,
      };
      break;
    case LOGOUT:
      state = initialState;
      break;
    case LOGOUT_SUCCESS:
      state = {
        ...state,
        user: null,
        accessToken: "",
        refreshToken: "",
      };
      break;
    case LOGOUT_FAIL:
      state = {
        ...state,
        error: {
          message: "Logout Failed",
        },
      };
      break;
    case CLEAR_ERROR:
      state = { ...state, error: { message: "" }, loading: false };
      break;
    case CLEAR_SIGN_UP_SUCCESS:
      state = { ...state, signUpSuccess: false };
      break;
    default:
      state = { ...state };
      break;
  }
  return state;
}
