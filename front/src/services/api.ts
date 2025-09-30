import axios from "axios";
import type { AxiosRequestConfig, AxiosResponse } from "axios";

// tokenService.ts
const ACCESS_TOKEN_KEY = "access_token";

export const tokenService = {
  set(token: string) {
    localStorage.setItem(ACCESS_TOKEN_KEY, token);
  },

  get(): string | null {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  },
};

async function request<T = any>(
  method: AxiosRequestConfig["method"],
  url: string,
  data?: any,
  headers: Record<string, string> = {}
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
    withCredentials: true,
  };

  try {
    const response = await axios(config);
    console.log(response.headers);
    if ('authorization' in response.headers){
      console.log(response.headers.authorization)
      tokenService.set(response.headers.authorization)
    }
    return response;
  } catch (error: any) {
    if (error.response) {
      console.error("Ошибка ответа:", error.response.data);
    } else {
      console.error("Ошибка запроса:", error.message);
    }
    throw error;
  }
}

export async function login(username: string, password: string){
  return request<{access_token: string; refresh_token: string}>(
    "post",
    "http://127.0.0.1:8000/user/sign_in",
    { login: username, password: password }
  )
}

export async function register(username: string, password1: string, password2: string){
  return request<{success: boolean}>(
    "post",
    "http://127.0.0.1:8000/user/sign_up",
    {login: username, password1: password1, password2: password2}
  )
}

export async function getNews(filters: any = {}){
  return request(
    "post",
    "http://127.0.0.1:8000/news/get",
    filters
  )
}
