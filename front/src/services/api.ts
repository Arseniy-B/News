import axios from "axios";
import type { AxiosRequestConfig, AxiosResponse } from "axios";

// tokenService.ts
const ACCESS_TOKEN_KEY = "access_token";

type Response = { status_code: number, detail: string}

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
  return request<{status_code: number; detail: Record<string, any> | any}>(
    "post",
    "http://127.0.0.1:8000/user/sign_in",
    { username: username, password: password }
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
    }
  )
}

export async function getNews(filters: any = {}){
  if (!("categories" in filters)){
    filters.categories = [];
  }
  return request(
    "post",
    "http://127.0.0.1:8000/news/get",
    filters
  )
}
