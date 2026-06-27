import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ItineraryResponse } from '@/types/itinerary'
import type { PaginatedResponse } from '@/types/common'
import { itineraryAPI } from '@/api/itinerary'

export const useItineraryStore = defineStore('itinerary', () => {
  const currentItinerary = ref<ItineraryResponse | null>(null)
  const itineraries = ref<ItineraryResponse[]>([])
  const total = ref(0)
  const loading = ref(false)
  const generating = ref(false)

  async function generateItinerary(query: string, userId?: string, itineraryId?: string) {
    generating.value = true
    try {
      const { data } = await itineraryAPI.generate(query, userId || 'anonymous', itineraryId)
      currentItinerary.value = data.data
      return data.data
    } finally {
      generating.value = false
    }
  }

  async function fetchItinerary(id: string) {
    loading.value = true
    try {
      const { data } = await itineraryAPI.getById(id)
      currentItinerary.value = data.data
      return data.data
    } finally {
      loading.value = false
    }
  }

  async function fetchItineraries(userId: string, page = 1, pageSize = 10): Promise<PaginatedResponse<ItineraryResponse>> {
    loading.value = true
    try {
      const { data } = await itineraryAPI.list(userId, page, pageSize)
      const result = data.data
      itineraries.value = result.items
      total.value = result.total
      return result
    } finally {
      loading.value = false
    }
  }

  async function updateItinerary(id: string, payload: any) {
    const { data } = await itineraryAPI.update(id, payload)
    currentItinerary.value = data.data
    return data.data
  }

  async function deleteItinerary(id: string) {
    await itineraryAPI.delete(id)
    itineraries.value = itineraries.value.filter((it) => it.id !== id)
  }

  return {
    currentItinerary,
    itineraries,
    total,
    loading,
    generating,
    generateItinerary,
    fetchItinerary,
    fetchItineraries,
    updateItinerary,
    deleteItinerary,
  }
})
