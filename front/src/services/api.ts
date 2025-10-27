import axios from "axios";
import type { AxiosRequestConfig, AxiosResponse } from "axios";
import type { NewsItem } from "../services/news-api/newsapi";


const ACCESS_TOKEN_KEY = "access_token";


export type Response<T> = { status_code: number, detail: string | null, data: T | null}

export const tokenService = {
  set(token: string) {
    localStorage.setItem(ACCESS_TOKEN_KEY, token);
  },
  get(): string | null {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  },
  delete() {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
  }
};


async function request<T = any>(
  method: AxiosRequestConfig["method"],
  url: string,
  data?: Record<string, any> | null,  // Более гибкий тип для params/body
  credentials: boolean = false,
  headers: Record<string, string> = {},
): Promise<AxiosResponse<T>> {

  const accessToken = tokenService.get();
  if (accessToken) {
    headers.Authorization = accessToken;
  }

  const config: AxiosRequestConfig = {
    method,
    url,
    headers,
    withCredentials: credentials,
  };

  // Для GET: data → params (query string); для остальных: data → body
  if (method === 'get' && data) {
    config.params = data;  // Axios сам построит ?q=val&page=1&...
  } else {
    config.data = data;
  }

  const response = await axios(config);

  // Сохраняем новый токен (headers в lowercase)
  if (response.headers.authorization) {
    tokenService.set(response.headers.authorization);
  }

  return response;
}

export async function login(username: string, password: string){
  return request<{status_code: number; detail: Record<string, any> | any}>(
    "post",
    "http://127.0.0.1:8000/user/sign_in",
    { username: username, password: password },
    true
  )
}

export async function register(username: string, email: string, password: string){
  return request<Response<any>>(
    "post",
    "http://127.0.0.1:8000/user/sign_up",
    {
      username: username, 
      email: email,
      password: password,
    },
    true
  )
}

export async function getNews(filters: any = {}){
  return request<Response<any>>(
    "post",
    "http://127.0.0.1:8000/news/get",
    filters
  )
}

export async function getTopHeadlinesNews(filters: any = {}){
  return request<Response<{news: NewsItem[], totalResults: number}>>(
    "post",
    "http://127.0.0.1:8000/news/top-headlines",
    filters
  )
}

export async function getUser(){
  return request<Response<any>>(
    "get",
    "http://127.0.0.1:8000/user/get",
    null,
    true
  )
}

export async function refreshToken(){
  return request<Response<any>>(
    "post",
    "http://127.0.0.1:8000/user/token",
    null,
    true
  )
}

export async function logout(){
  return request<Response<any>>(
    "post",
    "http://127.0.0.1:8000/user/logout",
    null,
    true
  )
}
