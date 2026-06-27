import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { paymentAPI } from '@/api/payment'
import type { Order, OrderItem, PaymentMethod } from '@/types/payment'

export const useBookingStore = defineStore('booking', () => {
  const currentOrder = ref<Order | null>(null)
  const orders = ref<Order[]>([])
  const loading = ref(false)
  const paying = ref(false)

  // 倒计时状态（15分钟）
  const countdown = ref(900) // 15 * 60
  let countdownTimer: ReturnType<typeof setInterval> | null = null

  // 计算属性
  const totalAmount = computed(() => {
    if (!currentOrder.value) return 0
    return currentOrder.value.items.reduce((sum, item) => sum + item.price, 0)
  })

  const formattedCountdown = computed(() => {
    const minutes = Math.floor(countdown.value / 60)
    const seconds = countdown.value % 60
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  })

  const isExpired = computed(() => countdown.value <= 0)

  // 创建订单
  async function createOrder(itineraryId: string, items: OrderItem[]) {
    loading.value = true
    try {
      const { data } = await paymentAPI.createOrder(itineraryId, items)
      currentOrder.value = data.data
      startCountdown()
      return data.data
    } catch (error) {
      console.error('创建订单失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取订单详情
  async function fetchOrder(orderId: string) {
    loading.value = true
    try {
      const { data } = await paymentAPI.getOrder(orderId)
      currentOrder.value = data.data
      return data.data
    } catch (error) {
      console.error('获取订单失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取订单列表
  async function fetchOrders(userId: string, page = 1, pageSize = 10) {
    loading.value = true
    try {
      const { data } = await paymentAPI.listOrders(userId, page, pageSize)
      orders.value = data.data.items
      return data.data
    } catch (error) {
      console.error('获取订单列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 支付订单
  async function payOrder(orderId: string, method: PaymentMethod) {
    paying.value = true
    try {
      const { data } = await paymentAPI.pay(orderId, method)
      currentOrder.value = data.data
      stopCountdown()
      return data.data
    } catch (error) {
      console.error('支付失败:', error)
      throw error
    } finally {
      paying.value = false
    }
  }

  // 取消订单
  async function cancelOrder(orderId: string) {
    try {
      const { data } = await paymentAPI.cancelOrder(orderId)
      currentOrder.value = null
      stopCountdown()
      return data.data
    } catch (error) {
      console.error('取消订单失败:', error)
      throw error
    }
  }

  // 启动倒计时
  function startCountdown() {
    stopCountdown()
    countdown.value = 900 // 重置为15分钟
    
    countdownTimer = setInterval(() => {
      if (countdown.value > 0) {
        countdown.value--
      } else {
        stopCountdown()
        // 倒计时结束，订单可能已被释放
        if (currentOrder.value) {
          currentOrder.value.status = 'expired'
        }
      }
    }, 1000)
  }

  // 停止倒计时
  function stopCountdown() {
    if (countdownTimer) {
      clearInterval(countdownTimer)
      countdownTimer = null
    }
  }

  // 清除当前订单
  function clearCurrentOrder() {
    currentOrder.value = null
    stopCountdown()
  }

  return {
    currentOrder,
    orders,
    loading,
    paying,
    countdown,
    totalAmount,
    formattedCountdown,
    isExpired,
    createOrder,
    fetchOrder,
    fetchOrders,
    payOrder,
    cancelOrder,
    startCountdown,
    stopCountdown,
    clearCurrentOrder,
  }
})
