import { ref, onUnmounted } from 'vue'
import { useNotificationStore } from '@/stores/notification'

const MAX_RECONNECT_DELAY = 30000 // 最大重连间隔 30s

export function useWebSocket(userId: string) {
  const ws = ref<WebSocket | null>(null)
  const connected = ref(false)
  const store = useNotificationStore()
  let reconnectAttempts = 0
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null

  function connect() {
    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:'
    const url = `${protocol}//${location.host}/api/v1/notification/ws/${userId}`
    ws.value = new WebSocket(url)

    ws.value.onopen = () => {
      connected.value = true
      reconnectAttempts = 0 // 连接成功后重置重试次数
    }

    ws.value.onmessage = (event) => {
      const message = JSON.parse(event.data)
      store.addNotification(message)
    }

    ws.value.onclose = () => {
      connected.value = false
      // 指数退避重连：1s, 2s, 4s, 8s, 16s, 30s, 30s...
      const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), MAX_RECONNECT_DELAY)
      reconnectAttempts++
      reconnectTimer = setTimeout(() => connect(), delay)
    }
  }

  function disconnect() {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }
    ws.value?.close()
    ws.value = null
  }

  onUnmounted(() => {
    disconnect()
  })

  return { connected, connect, disconnect }
}