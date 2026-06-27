export interface ActivityItem {
  id: string
  type: 'attraction' | 'restaurant' | 'hotel' | 'transport'
  name: string
  description: string
  address: string
  lat: number
  lng: number
  start_time: string
  end_time: string
  price: number
  tags: string[]
  notes: string
}

export interface DayItinerary {
  day_index: number
  date: string | null
  activities: ActivityItem[]
  hotel: ActivityItem | null
}

export interface ItineraryCreateRequest {
  title: string
  destination: string
  start_date: string | null
  end_date: string | null
  budget: number
  preferences: string[]
  constraints: string[]
  days: DayItinerary[]
}

export interface ItineraryResponse extends ItineraryCreateRequest {
  id: string
  user_id: string
  status: 'draft' | 'confirmed' | 'in_progress' | 'completed'
  total_budget: number
  version: number
  created_at: string
  updated_at: string
}