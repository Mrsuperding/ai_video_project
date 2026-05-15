export interface SendSmsCodeParams {
  phone: string
  type?: string
}

export interface LoginByPasswordParams {
  account: string
  password: string
  device_id?: string
  device_type?: string
  user_agent?: string
}

export interface LoginBySmsParams {
  phone: string
  sms_code: string
  device_id?: string
  device_type?: string
  invite_code?: string
}

export interface RegisterParams {
  phone: string
  password: string
  sms_code: string
  invite_code?: string
}

export interface LoginResponse {
  user: {
    id: number
    phone: string
    email?: string
    nickname: string
    avatar_url?: string
    membership_type: string
  }
  tokens: {
    access_token: string
    refresh_token: string
    expires_in: number
  }
}

export interface RefreshTokenParams {
  refresh_token: string
}