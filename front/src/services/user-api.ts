import type { BaseFilter } from "../services/news-api/newsapi";


export interface User{
  id: number
  username: string
  email: string
  created_at: Date
  updated_at: Date
  news_filters?: BaseFilter | null
}
