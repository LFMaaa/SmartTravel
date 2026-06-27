import client from './client'
import type { ApiResponse, PaginatedResponse, NotificationMessage } from '@/types/common'

export const notificationAPI = {
  getNotifications: (userId: string, page = 1, pageSize = 10) =>
    client.get<ApiResponse<PaginatedResponse<NotificationMessage>>>('/notification/notifications', { params: { user_id: userId, page, page_size: pageSize } }),
}