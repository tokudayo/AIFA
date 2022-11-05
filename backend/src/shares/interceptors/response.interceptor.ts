export interface Response<T> {
  data: T;
  pageSize: number | null;
  pageNumber: number | null;
  total: number;
  totalInactive?: number;
}
