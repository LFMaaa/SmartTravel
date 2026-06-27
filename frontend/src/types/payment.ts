export interface Order {
  id: string
  user_id: string
  items: OrderItem[]
  total_amount: number
  status: 'pending' | 'paid' | 'timeout' | 'cancelled' | 'expired'
  created_at: string
  expire_at: number
  paid_at?: string
}

export interface OrderItem {
  resource_type: string
  resource_id: string
  name: string
  price: number
  quantity: number
}

export type PaymentMethod = 'wechat' | 'alipay'