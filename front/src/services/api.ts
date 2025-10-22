import axios from "axios";
import type { AxiosRequestConfig, AxiosResponse } from "axios";


const ACCESS_TOKEN_KEY = "access_token";


export type Response = { status_code: number, detail: string | null, data: any | null}

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
  data?: any,
  credentials: boolean = false,
  headers: Record<string, string> = {},
): Promise<AxiosResponse<T>> {

  const accessToken = tokenService.get();
  if (accessToken){
    headers.Authorization = accessToken;
  }

  const config: AxiosRequestConfig = {
    method,
    url,
    data,
    headers,
    withCredentials: credentials,
  };

  const response = await axios(config);
  if ('authorization' in response.headers){
    tokenService.set(response.headers.authorization)
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
  return request<Response>(
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
  if (!("categories" in filters)){
    filters.categories = [];
  }
  return request<Response>(
    "post",
    "http://127.0.0.1:8000/news/get",
    filters
  )
}

export async function getUser(){
  return request<Response>(
    "get",
    "http://127.0.0.1:8000/user/get",
    null,
    true
  )
}

export async function refreshToken(){
  return request<Response>(
    "post",
    "http://127.0.0.1:8000/user/token",
    null,
    true
  )
}

export async function logout(){
  return request<Response>(
    "post",
    "http://127.0.0.1:8000/user/logout",
    null,
    true
  )
}
