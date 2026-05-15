import request from '../request'

export interface WalletInfo {
  balance: string
  frozen_balance: string
  total_recharge: string
  total_consume: string
}

export interface WalletTransaction {
  id: number
  transaction_no: string
  transaction_type: string
  amount: string
  balance_before: string
  balance_after: string
  related_type: string
  related_id: number
  remark: string
  created_at: string
}

export interface RechargeOrder {
  order_no: string
  amount: string
  payment_method: string
  payment_info: {
    qr_code: string
    expire_time: string
  }
}

export const getWalletInfo = () =>
  request.get<WalletInfo>('/wallet')

export const getWalletTransactions = (params?: {
  transaction_type?: string
  start_date?: string
  end_date?: string
  page?: number
  page_size?: number
}) =>
  request.get<{ items: WalletTransaction[]; pagination: any }>('/wallet/transactions', { params })

export const createRechargeOrder = (data: {
  amount: string
  payment_method: string
}) =>
  request.post<RechargeOrder>('/wallet/recharge', data)

export const getRechargeStatus = (orderNo: string) =>
  request.get<{ order_no: string; amount: string; status: string; paid_at: string }>(`/wallet/recharge/${orderNo}`)

export const getUserQuota = () =>
  request.get('/user/quota')