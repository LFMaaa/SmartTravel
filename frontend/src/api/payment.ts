import client from './client'
import type { ApiResponse, PaginatedResponse } from '@/types/common'
import type { Order, OrderItem, PaymentMethod } from '@/types/payment'

export interface MemberOrderResult {
  order_id: string
  total_amount: number
  alipay_url: string | null
  sandbox_mode: boolean
}

export const paymentAPI = {
  createOrder: (itineraryId: string, items: OrderItem[]) =>
    client.post<ApiResponse<Order>>('/payment/orders', {
      itinerary_id: itineraryId,
      items,
    }),

  getOrder: (id: string) =>
    client.get<ApiResponse<Order>>(`/payment/orders/${id}`),

  pay: (id: string, method: PaymentMethod) =>
    client.post<ApiResponse<Order>>(`/payment/orders/${id}/pay`, { method }),

  cancelOrder: (id: string) =>
    client.post<ApiResponse<Order>>(`/payment/orders/${id}/cancel`),

  listOrders: (userId: string, page = 1, pageSize = 10) =>
    client.get<ApiResponse<PaginatedResponse<Order>>>('/payment/orders', {
      params: { user_id: userId, page, page_size: pageSize },
    }),

  // 会员支付
  createMemberOrder: (userId: string) =>
    client.post<ApiResponse<MemberOrderResult>>('/payment/member/create', {
      user_id: userId,
    }),

  getMemberPayStatus: (orderId: string) =>
    client.get<ApiResponse<{ order_id: string; status: string; paid_at: string | null }>>(
      `/payment/member/status/${orderId}`
    ),

  // 沙箱模拟支付（开发环境）
  sandboxPayMember: (orderId: string) =>
    client.post<ApiResponse<{ order_id: string; status: string; is_pro: boolean }>>(
      `/payment/member/sandbox-pay/${orderId}`
    ),

  // 预订支付
  createBookingOrder: (params: {
    user_id: string
    itinerary_id?: string
    total_amount: number
    items: Array<{
      resource_type: string
      resource_id?: string
      resource_name: string
      unit_price: number
      quantity: number
    }>
    return_url?: string
  }) =>
    client.post<ApiResponse<MemberOrderResult>>('/payment/booking/create', params),

  getBookingPayStatus: (orderId: string) =>
    client.get<ApiResponse<{ order_id: string; status: string; paid_at: string | null }>>(
      `/payment/booking/status/${orderId}`
    ),

  sandboxPayBooking: (orderId: string) =>
    client.post<ApiResponse<{ order_id: string; status: string }>>(
      `/payment/booking/sandbox-pay/${orderId}`
    ),
}