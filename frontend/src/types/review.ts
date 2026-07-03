export interface ReviewReply {
  id: string
  user_id: string
  user_name: string
  user_avatar: string | null
  content: string
  likes: number
  created_at: string
  reply_to: string
}

export interface ReviewItem {
  id: string
  poi_id: string
  user_id: string
  user_name: string
  user_avatar: string | null
  content: string
  rating: number | null
  likes: number
  created_at: string
  replies: ReviewReply[]
}

export interface ReviewListData {
  items: ReviewItem[]
  total: number
  avg_rating: number
  page: number
  page_size: number
}
