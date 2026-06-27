import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { NotificationMessage } from '@/types/common'

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref<NotificationMessage[]>([])
  const unreadCount = ref(0)

  function addNotification(msg: NotificationMessage) {
    notifications.value.unshift(msg)
    unreadCount.value++
  }

  function markAsRead(id: string) {
    const n = notifications.value.find((n) => n.id === id)
    if (n && !n.read) {
      n.read = true
      unreadCount.value--
    }
  }

  return { notifications, unreadCount, addNotification, markAsRead }
})