export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface PaginatedResponse<T = any> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface UserInfo {
  id: string
  phone: string
  nickname: string
  avatar: string | null
  is_pro: boolean
  pro_expire_at: string | null
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface RegisterResponse {
  phone: string
  message: string
}

export interface NotificationMessage {
  id: string
  type: string
  title: string
  content: string
  created_at: string
  read: boolean
}