import axios from "axios";
import type { AxiosRequestConfig, AxiosResponse } from "axios";

// Универсальная функция для запросов
async function request<T = any>(
  method: AxiosRequestConfig["method"],
  url: string,
  data?: any,
  headers?: Record<string, string>
): Promise<AxiosResponse<T>> {
  const config: AxiosRequestConfig = {
    method,
    url,
    data,
    headers,
  };

  try {
    const response = await axios(config);
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

