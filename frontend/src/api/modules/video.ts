import request from '../request'
import type {
  VideoProject,
  CreateVideoProjectParams,
  UpdateVideoProjectParams
} from './types/video'

export const getVideoProjects = (params?: {
  status?: string
  category?: string
  keyword?: string
  page?: number
  page_size?: number
}) =>
  request.get<{ items: VideoProject[]; pagination: any }>('/video-projects', { params })

export const getVideoProjectDetail = (id: number) =>
  request.get<VideoProject>(`/video-projects/${id}`)

export const createVideoProject = (params: CreateVideoProjectParams) =>
  request.post<{ id: number }>('/video-projects', params)

export const updateVideoProject = (id: number, params: UpdateVideoProjectParams) =>
  request.patch<VideoProject>(`/video-projects/${id}`, params)

export const deleteVideoProject = (id: number) =>
  request.delete(`/video-projects/${id}`)

export const submitVideoGenerate = (id: number, params?: { priority?: number }) =>
  request.post<{ task_id: number }>(`/video-projects/${id}/generate`, params)

export const cancelVideoGenerate = (id: number) =>
  request.post(`/video-projects/${id}/cancel`)

export const getVideoOutput = (projectId: number) =>
  request.get(`/video-projects/${projectId}/output`)