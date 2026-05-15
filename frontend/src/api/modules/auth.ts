import request from '../request'
import type {
  SendSmsCodeParams,
  LoginByPasswordParams,
  LoginBySmsParams,
  LoginResponse,
  RefreshTokenParams,
  RegisterParams
} from './types/auth'

// Auth APIs
export const sendSmsCode = (params: SendSmsCodeParams) =>
  request.post('/auth/sms/send', params)

export const loginByPassword = (params: LoginByPasswordParams) =>
  request.post<LoginResponse>('/auth/login/password', params)

export const loginBySms = (params: LoginBySmsParams) =>
  request.post<LoginResponse>('/auth/login/sms', params)

export const register = (params: RegisterParams) =>
  request.post('/auth/register', params)

export const refreshToken = (params: RefreshTokenParams) =>
  request.post<{ access_token: string; refresh_token: string }>('/auth/refresh', params)

export const logout = () =>
  request.post('/auth/logout')