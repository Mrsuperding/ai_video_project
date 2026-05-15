import request from '../request'
import type {
  UserProfile,
  UpdateProfileParams,
  ChangePasswordParams
} from './types/user'

export const getProfile = () =>
  request.get<UserProfile>('/user/profile')

export const updateProfile = (params: UpdateProfileParams) =>
  request.patch<UserProfile>('/user/profile', params)

export const updateAvatar = (avatarUrl: string) =>
  request.post<{ avatar_url: string }>('/user/avatar', { avatar_url: avatarUrl })

export const changePassword = (params: ChangePasswordParams) =>
  request.post('/user/password', params)

export const getUserQuota = () =>
  request.get('/user/quota')