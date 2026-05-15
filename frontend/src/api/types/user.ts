export interface UserProfile {
  id: number
  phone: string
  email?: string
  nickname: string
  avatar_url?: string
  real_name?: string
  id_card_number?: string
  real_name_verified: boolean
  membership_type: string
  membership_expire_at?: string
  balance: string
  frozen_balance: string
  quota: {
    digital_human: { total: number; used: number; remaining: number }
    video_monthly: { total: number; used: number; remaining: number }
  }
}

export interface UpdateProfileParams {
  nickname?: string
  email?: string
  real_name?: string
}

export interface ChangePasswordParams {
  old_password: string
  new_password: string
}