import request from '../request'

export interface AdminUser {
  id: number
  phone: string
  email: string | null
  nickname: string
  avatar_url: string | null
  membership_type: string
  status: string
  balance: string
  created_at: string
  last_login_at: string | null
}

export interface AdminStatistics {
  period: string
  start_date: string
  end_date: string
  users: {
    new: number
    active: number
    paid: number
    churned: number
  }
  business: {
    video_projects_created: number
    video_projects_completed: number
    video_projects_failed: number
    video_success_rate: number
    digital_humans_created: number
    avg_video_duration: number
  }
  finance: {
    total_revenue_cents: number
    membership_revenue_cents: number
    single_purchase_revenue_cents: number
    total_cost_cents: number
    gross_profit_cents: number
  }
  models: Record<string, {
    calls: number
    success: number
    fail: number
    success_rate: number
    cost_cents: number
  }>
}

export const adminLogin = (username: string, password: string) =>
  request.post<{ admin: any; tokens: any }>('/admin/login', { username, password })

export const getAdminUsers = (params?: {
  keyword?: string
  membership_type?: string
  status?: string
  page?: number
  page_size?: number
}) =>
  request.get<{ items: AdminUser[]; pagination: any }>('/admin/users', { params })

export const getAdminUserDetail = (userId: number) =>
  request.get<AdminUser>(`/admin/users/${userId}`)

export const banAdminUser = (userId: number, action: 'ban' | 'unban') =>
  request.post(`/admin/users/${userId}/ban`, { action })

export const getPlatformStatistics = (params?: {
  period?: string
  start_date?: string
  end_date?: string
}) =>
  request.get<AdminStatistics>('/admin/statistics/overview', { params })

export const getAdminConfigs = () =>
  request.get<{ items: any[] }>('/admin/configs')

export const updateAdminConfigs = (configs: Record<string, string>[]) =>
  request.patch('/admin/configs', { configs })