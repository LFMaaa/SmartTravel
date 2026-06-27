import client from './client'
import type { ApiResponse, PaginatedResponse } from '@/types/common'
import type { POIResult } from '@/types/search'

export const searchAPI = {
  searchPOI: (params: Record<string, any>) =>
    client.get<ApiResponse<PaginatedResponse<POIResult>>>('/search/poi', { params }),

  searchNearby: (params: Record<string, any>) =>
    client.get<ApiResponse<PaginatedResponse<POIResult>>>('/search/poi/nearby', { params }),

  suggest: (keyword: string, size = 5) =>
    client.get<ApiResponse<string[]>>('/search/suggest', { params: { keyword, size } }),
}