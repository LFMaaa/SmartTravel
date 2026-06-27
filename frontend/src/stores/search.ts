import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { POIResult } from '@/types/search'
import { searchAPI } from '@/api/search'

export const useSearchStore = defineStore('search', () => {
  const results = ref<POIResult[]>([])
  const total = ref(0)
  const loading = ref(false)

  async function search(params: Record<string, any>) {
    loading.value = true
    try {
      const { data } = await searchAPI.searchPOI(params)
      results.value = data.data.items
      total.value = data.data.total
    } finally {
      loading.value = false
    }
  }

  async function suggest(keyword: string) {
    const { data } = await searchAPI.suggest(keyword)
    return data.data
  }

  return { results, total, loading, search, suggest }
})