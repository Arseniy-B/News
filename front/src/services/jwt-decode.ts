export interface JwtPayload {
  sub?: string;  // Пример полей: subject
  iat?: number;  // issued at
  exp?: number;  // expiration
  [key: string]: any;  // Для произвольных полей
}

export function decodeJwt(token: string): JwtPayload | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) {
      throw new Error('Invalid JWT token');
    }

    // Берем вторую часть (payload)
    const payload = parts[1];

    // Base64Url -> Base64 (заменяем - и _ на + и /, добавляем padding)
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = Buffer.from(base64, 'base64').toString('utf8');

    // Парсим JSON
    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('JWT decode error:', error);
    return null;
  }
}
