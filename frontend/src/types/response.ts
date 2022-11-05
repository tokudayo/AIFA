import { User } from "./user";

export interface Pagination {
  total_count: number;
  limit_value: number;
  total_pages: number;
  current_page: number;
}

export interface LoginResponse {
  accessToken: string;
  refreshToken: string;
  user: User;
}