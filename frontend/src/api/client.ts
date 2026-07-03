import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, InternalAxiosRequestConfig } from 'axios'

const baseURL = '/api/v1'

const client: AxiosInstance = axios.create({
  baseURL,
  timeout: 10000,
})

// 请求拦截器：自动附加 Token（同时支持标准 Bearer 和 x-user-token）
client.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem('access_token')
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
    // 部分服务（如 review-service）通过自定义 header 获取 token
    config.headers['x-user-token'] = token
  }
  return config
})

// 响应拦截器：Token 过期自动刷新
let isRefreshing = false
let refreshSubscribers: ((token: string) => void)[] = []

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve) => {
          refreshSubscribers.push((token: string) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            resolve(client(originalRequest))
          })
        })
      }
      originalRequest._retry = true
      isRefreshing = true
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        const { data } = await axios.post(`${baseURL}/user/refresh`, { refresh_token: refreshToken })
        const newToken = data.data.access_token
        localStorage.setItem('access_token', newToken)
        refreshSubscribers.forEach((cb) => cb(newToken))
        refreshSubscribers = []
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return client(originalRequest)
      } catch {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(error)
      } finally {
        isRefreshing = false
      }
    }
    return Promise.reject(error)
  },
)

export default client