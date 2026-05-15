import request from '../request'
import type { Script, CreateScriptParams, UpdateScriptParams } from './types/script'

export const getScripts = (params?: {
  page?: number
  page_size?: number
  keyword?: string
  category?: string
}) =>
  request.get<{ items: Script[]; pagination: any }>('/scripts', { params })

export const getScriptDetail = (id: number) =>
  request.get<Script>(`/scripts/${id}`)

export const createScript = (params: CreateScriptParams) =>
  request.post<{ id: number }>('/scripts', params)

export const updateScript = (id: number, params: UpdateScriptParams) =>
  request.patch<Script>(`/scripts/${id}`, params)

export const deleteScript = (id: number) =>
  request.delete(`/scripts/${id}`)

export const saveScriptAsTemplate = (id: number, data: { name: string; description?: string; category?: string }) =>
  request.post(`/scripts/${id}/save-as-template`, data)

export const getScriptTemplates = (params?: { page?: number; page_size?: number; category?: string }) =>
  request.get<{ items: any[]; pagination: any }>('/script-templates', { params })

export const getScriptTemplateDetail = (id: number) =>
  request.get<any>(`/script-templates/${id}`)

export const generateScriptByAI = (data: {
  input_type: string
  template_id?: number
  template_params?: Record<string, any>
  input_prompt?: string
  style?: string
  emotion?: string
  target_language?: string
  duration_seconds?: number
}) => request.post('/scripts/generate', data)

export const rewriteScriptByAI = (data: {
  text: string
  task_type: string
  style?: string
  target_language?: string
}) => request.post('/scripts/rewrite', data)

export const getAITaskStatus = (taskId: number) =>
  request.get(`/scripts/tasks/${taskId}`)