import client from './client'
import type { ApiResponse } from '@/types/common'
import type { ReviewListData, ReviewItem } from '@/types/review'

export const reviewAPI = {
  getReviews: (poiId: string, page = 1, pageSize = 20) =>
    client.get<ApiResponse<ReviewListData>>(`/review/poi/${poiId}`, { params: { page, page_size: pageSize } }),

  createReview: (poiId: string, content: string, rating?: number, parentId?: string) =>
    client.post<ApiResponse<ReviewItem>>(`/review/poi/${poiId}`, { content, rating, parent_id: parentId }),

  deleteReview: (reviewId: string) =>
    client.delete(`/review/${reviewId}`),

  likeReview: (reviewId: string) =>
    client.post<ApiResponse<{ likes: number }>>(`/review/${reviewId}/like`),
}
