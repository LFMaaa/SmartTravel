import client from './client'
import type { ApiResponse, TokenResponse, RegisterResponse, UserInfo } from '@/types/common'

export const userAPI = {
  // Password auth — register requires SMS verification code
  register: (phone: string, password: string, smsCode: string, nickname = '') =>
    client.post<ApiResponse<RegisterResponse>>('/user/register', { phone, password, sms_code: smsCode, nickname }),

  login: (phone: string, password: string) =>
    client.post<ApiResponse<TokenResponse>>('/user/login', { phone, password }),

  // SMS auth
  sendSmsCode: (phone: string) =>
    client.post<ApiResponse<{ phone: string; code?: string; expires_in: number }>>('/user/sms/send', { phone }),

  verifySmsCode: (phone: string, code: string) =>
    client.post<ApiResponse<{ verified: boolean; message: string }>>('/user/sms/verify', { phone, code }),

  loginBySms: (phone: string, code: string) =>
    client.post<ApiResponse<TokenResponse>>('/user/sms/login', { phone, code }),

  // WeChat auth
  loginByWechat: (code: string, nickname?: string, avatarUrl?: string) =>
    client.post<ApiResponse<TokenResponse>>('/user/wechat/login', {
      code,
      nickname: nickname || '',
      avatar_url: avatarUrl || '',
    }),

  // Token management
  refresh: (refreshToken: string) =>
    client.post<ApiResponse<TokenResponse>>('/user/refresh', { refresh_token: refreshToken }),

  getMe: () =>
    client.get<ApiResponse<UserInfo>>('/user/me'),

  updatePreferences: (data: Record<string, any>) =>
    client.put<ApiResponse<null>>('/user/preferences', data),
}
