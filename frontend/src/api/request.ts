import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import type { AxiosError } from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

let isRefreshing = false
let refreshSubscribers: ((token: string) => void)[] = []

function subscribeTokenRefresh(callback: (token: string) => void) {
  refreshSubscribers.push(callback)
}

function onTokenRefreshed(token: string) {
  refreshSubscribers.forEach(callback => callback(token))
  refreshSubscribers = []
}

class Request {
  private instance: AxiosInstance

  constructor() {
    this.instance = axios.create({
      baseURL: BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // Request interceptor
    this.instance.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // Response interceptor
    this.instance.interceptors.response.use(
      (response: AxiosResponse<ApiResponse>) => {
        const { code, message, data } = response.data

        if (code !== 0 && code !== 200) {
          ElMessage.error(message || '请求失败')
          return Promise.reject(new Error(message))
        }

        return response.data
      },
      async (error: AxiosError<ApiResponse>) => {
        const originalRequest = error.config as any

        if (error.response?.status === 401 && !originalRequest._retry) {
          if (isRefreshing) {
            // Wait for token refresh to complete
            return new Promise((resolve, reject) => {
              subscribeTokenRefresh((token: string) => {
                originalRequest.headers.Authorization = `Bearer ${token}`
                resolve(this.instance(originalRequest))
              })
            })
          }

          originalRequest._retry = true
          isRefreshing = true

          try {
            const refreshToken = localStorage.getItem('refresh_token')
            if (!refreshToken) {
              throw new Error('No refresh token')
            }

            const response = await axios.post(`${BASE_URL}/auth/refresh`, {
              refresh_token: refreshToken
            })

            const { data } = response.data
            if (data?.access_token) {
              localStorage.setItem('token', data.access_token)
              if (data.refresh_token) {
                localStorage.setItem('refresh_token', data.refresh_token)
              }
              onTokenRefreshed(data.access_token)

              originalRequest.headers.Authorization = `Bearer ${data.access_token}`
              return this.instance(originalRequest)
            }

            throw new Error('Invalid refresh response')
          } catch (refreshError) {
            // Refresh failed, logout
            localStorage.removeItem('token')
            localStorage.removeItem('refresh_token')
            ElMessage.error('登录已过期，请重新登录')
            router.push('/auth/login')
            return Promise.reject(refreshError)
          } finally {
            isRefreshing = false
          }
        }

        if (error.response) {
          const { status, data } = error.response

          switch (status) {
            case 403:
              ElMessage.error('没有权限访问')
              break
            case 404:
              ElMessage.error('请求的资源不存在')
              break
            case 500:
              ElMessage.error('服务器错误')
              break
            default:
              ElMessage.error(data?.message || '请求失败')
          }
        } else {
          ElMessage.error('网络错误，请检查网络连接')
        }

        return Promise.reject(error)
      }
    )
  }

  public get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.get(url, config).then((res) => res.data)
  }

  public post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.post(url, data, config).then((res) => res.data)
  }

  public put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.put(url, data, config).then((res) => res.data)
  }

  public patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.patch(url, data, config).then((res) => res.data)
  }

  public delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.delete(url, config).then((res) => res.data)
  }
}

export default new Request()