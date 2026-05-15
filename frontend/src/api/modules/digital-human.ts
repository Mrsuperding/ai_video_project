import request from '../request'
import type {
  DigitalHuman,
  CreateDigitalHumanParams,
  UpdateDigitalHumanParams
} from './types/digital-human'

export const getDigitalHumans = (params?: { page?: number; page_size?: number; keyword?: string; status?: string }) =>
  request.get<{ items: DigitalHuman[]; pagination: any }>('/digital-humans', { params })

export const getDigitalHumanDetail = (id: number) =>
  request.get<DigitalHuman>(`/digital-humans/${id}`)

export const createDigitalHuman = (params: CreateDigitalHumanParams) =>
  request.post<{ id: number }>('/digital-humans', params)

export const updateDigitalHuman = (id: number, params: UpdateDigitalHumanParams) =>
  request.patch<DigitalHuman>(`/digital-humans/${id}`, params)

export const deleteDigitalHuman = (id: number) =>
  request.delete(`/digital-humans/${id}`)

export const generateDigitalHuman = (id: number, params?: { priority?: number }) =>
  request.post<{ task_id: number }>(`/digital-humans/${id}/generate`, params)

export const getDigitalHumanTemplates = () =>
  request.get<{ items: any[] }>('/digital-human/templates')