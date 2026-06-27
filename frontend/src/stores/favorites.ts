import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { POIResult } from '@/types/search'

const STORAGE_KEY = 'smarttravel_favorites'

function loadFromStorage(): POIResult[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function saveToStorage(items: POIResult[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
}

export const useFavoritesStore = defineStore('favorites', () => {
  const items = ref<POIResult[]>(loadFromStorage())

  function isFavorite(id: string): boolean {
    return items.value.some((i) => i.id === id)
  }

  function addFavorite(poi: POIResult) {
    if (isFavorite(poi.id)) return
    items.value.push(poi)
    saveToStorage(items.value)
  }

  function removeFavorite(id: string) {
    items.value = items.value.filter((i) => i.id !== id)
    saveToStorage(items.value)
  }

  function toggleFavorite(poi: POIResult) {
    if (isFavorite(poi.id)) {
      removeFavorite(poi.id)
    } else {
      addFavorite(poi)
    }
  }

  return { items, isFavorite, addFavorite, removeFavorite, toggleFavorite }
})
