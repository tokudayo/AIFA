import { User } from "../types/user";

export default class StorageUtils {
  static setItem(key: string, value: string) {
    window.localStorage.setItem(key, value);
  }

  static getItem(key: string, defaultValue: string) {
    const result = window.localStorage.getItem(key);
    if (result === null || result === undefined) return defaultValue;
    return result;
  }

  static removeItem(key: string) {
    window.localStorage.removeItem(key);
  }

  // section storage
  static setSectionStorageItem(key: string, value: string) {
    window.sessionStorage.setItem(key, value);
  }

  static getSectionStorageItem(key: string) {
    return window.sessionStorage.getItem(key);
  }

  static removeSectionStorageItem(key: string) {
    window.sessionStorage.removeItem(key);
  }

  static setUser(value: User) {
    this.setSectionStorageItem('USER', JSON.stringify(value));
  }

  static getUser() {
    const user = this.getSectionStorageItem('USER') as string;
    return JSON.parse(user);
  }

  static removeUser() {
    this.removeSectionStorageItem('USER');
  }

  // Token
  static setToken(value = "") {
    StorageUtils.setSectionStorageItem('ACCESS_TOKEN', value);
  }

  static getToken() {
    return StorageUtils.getSectionStorageItem('ACCESS_TOKEN');
  }

  static removeToken() {
    StorageUtils.removeSectionStorageItem('ACCESS_TOKEN');
  }

  static setRefreshToken(value = "") {
    StorageUtils.setSectionStorageItem('REFRESH_TOKEN', value);
  }

  static getRefreshToken() {
    return StorageUtils.getSectionStorageItem('REFRESH_TOKEN');
  }

  static removeRefreshToken() {
    StorageUtils.removeSectionStorageItem('REFRESH_TOKEN');
  }
}
