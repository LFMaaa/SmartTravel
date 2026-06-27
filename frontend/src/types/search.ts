export interface POIResult {
  id: string
  name: string
  type: string
  city: string
  district?: string
  rating: number
  price: number
  tags: string[]
  lat: number
  lng: number
  distance?: string
  description?: string
  address?: string
  opening_hours?: string
  popularity_score?: number
}

export interface SearchParams {
  keyword: string
  city?: string
  poi_type?: string
  page?: number
  page_size?: number
}

export interface NearbyParams {
  lat: number
  lng: number
  radius?: number
  poi_type?: string
  page?: number
  page_size?: number
}
