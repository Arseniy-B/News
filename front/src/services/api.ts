import axios from "axios";
import type { AxiosRequestConfig, AxiosResponse } from "axios";
import type { NewsItem } from "../services/news-api/newsapi";
import type { TopHeadlinesFilter, EverythingFilter} from "@/services/news-api/newsapi";


const ACCESS_TOKEN_KEY = "access_token";
const BASE_URL = "http://178.72.150.69/api";


export type Response<T> = { detail: string | null, data: T | null}

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


async function request<T = any>(opts: {
  method: AxiosRequestConfig["method"],
  url: string,
  data?: Record<string, any> | null,
  params?: Record<string, any>,
  credentials: boolean,
  headers?: Record<string, string>,
}): Promise<AxiosResponse<T>> {

  opts.headers = {}
  const accessToken = tokenService.get();
  if (accessToken) {
    opts.headers.Authorization = accessToken;
  }

  const config: AxiosRequestConfig = {
    method: opts.method,
    url: BASE_URL + opts.url,
    headers: opts.headers,
    withCredentials: opts.credentials,
  };

  config.params = opts.params || (opts.method === 'get' && opts.data ? opts.data : undefined);

  if (opts.method !== 'get') {
    config.data = opts.data;
  }
  const response = await axios(config);
  if (response.headers.authorization) {
    tokenService.set(response.headers.authorization);
  }
  return response;
}

export async function login_by_password(username: string, password: string){
  return request<{status_code: number; detail: Record<string, any> | any}>({
    method: "post",
    url: "/auth/sign_in",
    data: { username: username, password: password },
    credentials: true
  })
}

export async function login_by_email(email: string, code: string){
  return request<{status_code: number; detail: Record<string, any> | any}>({
    method: "post",
    url: "/auth/email/sign_in",
    data: { email: email, code: code},
    credentials: true
  })
}
export async function send_otp(email: string){
  return request({
    method: "post",
    url: "/auth/email/send_otp",
    data: {email: email},
    credentials: false
  })
}

export async function register(username: string, email: string, password: string){
  return request<Response<any>>({
    method: "post",
    url: "/auth/sign_up",
    data: {
      username: username, 
      email: email,
      password: password,
    },
    credentials: true
  })
}

export async function getTopHeadlinesNews(filters: any = {}){
  return request<Response<{news: NewsItem[], totalResults: number}>>({
    method: "post",
    url: "/news/get",
    data: filters,
    params: {filter_type: "TopHeadlines"},
    credentials: false
  })
}

export async function getEverythingNews(filters: any={}){
  return request<Response<{news: NewsItem[], totalResults: number}>>({
    method: "post",
    url: "/news/get",
    data: filters,
    params: {filter_type: "Everything"},
    credentials: false
  })
}

export async function getUser(){
  return request<Response<any>>({
    method: "get",
    url: "/user/get",
    credentials: true
  })
}

export async function refreshToken(){
  return request<Response<any>>({
    method: "post",
    url: "/auth/token",
    credentials: true
  })
}

export async function logout(){
  return request<Response<any>>({
    method: "post",
    url: "/auth/logout",
    credentials: true
  })
}


export async function setUserFilters(filters: any = {}, filter_type: string){
  return request<Response<any>>({
    method: "post",
    url: "/user/set-filters",
    data: filters,
    params: {filter_type: filter_type},
    credentials: true 
  })
}

export async function getUserFilters(filterTypes: string[]){
  return request<Response<(TopHeadlinesFilter | EverythingFilter)[]>>({
    method: "post",
    url: "/user/get-filters",
    data: filterTypes,
    credentials: true
  })
}
