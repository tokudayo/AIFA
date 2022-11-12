import { User } from "../types/user";

export default class StorageUtils {
  static setItem(key: string, value: string) {
    window.localStorage.setItem(key, value);
  }

  static getItem(key: string) {
    return window.localStorage.getItem(key);
  }

  static removeItem(key: string) {
    window.localStorage.removeItem(key);
  }

  static setUser(value: User) {
    this.setItem("USER", JSON.stringify(value));
  }

  static getUser() {
    const user = this.getItem("USER") as string;
    return JSON.parse(user);
  }

  static removeUser() {
    this.removeItem("USER");
  }

  // Token
  static setToken(value = "") {
    this.setItem("ACCESS_TOKEN", value);
  }

  static getToken() {
    return this.getItem("ACCESS_TOKEN");
  }

  static removeToken() {
    this.removeItem("ACCESS_TOKEN");
  }

  static setRefreshToken(value = "") {
    this.setItem("REFRESH_TOKEN", value);
  }

  static getRefreshToken() {
    return this.getItem("REFRESH_TOKEN");
  }

  static removeRefreshToken() {
    this.removeItem("REFRESH_TOKEN");
  }
}
