export interface JwtPayload {
  sub: string;  // Пример полей: subject
  iat: number;  // issued at
  exp: number;  // expiration
  [key: string]: any;  // Для произвольных полей
}

export function decodeJwt(token: string): JwtPayload | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) {
      throw new Error('Invalid JWT token');
    }

    // Берем вторую часть (payload)
    let payload = parts[1];

    // Base64Url -> Base64 (корректировка символов)
    payload += '='.repeat((4 - payload.length % 4) % 4);  // Добавляем padding
    payload = payload.replace(/-/g, '+').replace(/_/g, '/');

    // Декодируем: в Node.js используй Buffer, в браузере — atob
    let jsonPayload: string;
    if (typeof Buffer !== 'undefined') {
      // Node.js
      jsonPayload = Buffer.from(payload, 'base64').toString('utf8');
    } else {
      // Браузер
      jsonPayload = atob(payload);
    }

    // Парсим JSON
    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('JWT decode error:', error);
    return null;
  }
}
