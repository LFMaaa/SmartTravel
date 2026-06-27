import { paymentAPI } from '@/api/payment'
import type { Order } from '@/types/payment'

export function usePayment() {
  async function createOrder(orderData: Record<string, any>): Promise<Order> {
    const { data } = await paymentAPI.createOrder(orderData.itinerary_id, orderData.items)
    return data.data
  }

  async function payOrder(orderId: string) {
    const { data } = await paymentAPI.pay(orderId, 'wechat' as any)
    return data.data
  }

  async function cancelOrder(orderId: string) {
    await paymentAPI.cancelOrder(orderId)
  }

  return { createOrder, payOrder, cancelOrder }
}