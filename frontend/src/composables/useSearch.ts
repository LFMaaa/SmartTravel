import { useSearchStore } from '@/stores/search'

export function useSearch() {
  const store = useSearchStore()

  async function search(keyword: string, city?: string, poiType?: string, page = 1, pageSize = 10) {
    return store.search({ keyword, city, poi_type: poiType, page, page_size: pageSize })
  }

  async function suggest(keyword: string, size?: number) {
    return store.suggest(keyword, size)
  }

  return { ...store, search, suggest }
}