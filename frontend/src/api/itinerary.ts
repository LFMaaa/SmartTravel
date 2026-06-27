import client from './client'
import type { ApiResponse, PaginatedResponse } from '@/types/common'
import type { ItineraryCreateRequest, ItineraryResponse } from '@/types/itinerary'

export const itineraryAPI = {
  generate: (query: string, userId?: string, itineraryId?: string) =>
    client.post<ApiResponse<ItineraryResponse>>('/itinerary/generate', { query, user_id: userId || 'anonymous', itinerary_id: itineraryId || '' }),

  generateStream: (query: string) =>
    client.post('/itinerary/generate/stream', { query }, { responseType: 'stream' }),

  getById: (id: string) =>
    client.get<ApiResponse<ItineraryResponse>>(`/itinerary/${id}`),

  update: (id: string, data: ItineraryCreateRequest) =>
    client.put<ApiResponse<ItineraryResponse>>(`/itinerary/${id}`, data),

  delete: (id: string) =>
    client.delete(`/itinerary/${id}`),

  list: (userId: string, page = 1, pageSize = 10) =>
    client.get<ApiResponse<PaginatedResponse<ItineraryResponse>>>('/itinerary/', { params: { user_id: userId, page, page_size: pageSize } }),

  replan: (itineraryId: string, eventType: string, eventDetail: Record<string, any>) =>
    client.post(`/itinerary/${itineraryId}/replan`, { itinerary_id: itineraryId, event_type: eventType, event_detail: eventDetail }),
}
