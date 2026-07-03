<template>
  <router-view v-slot="{ Component, route }">
    <transition name="page-fade" mode="out-in">
      <component :is="Component" :key="route.path" />
    </transition>
  </router-view>
  <NotificationToast ref="toastRef" />
</template>

<script setup lang="ts">
import { ref, provide } from 'vue'
import NotificationToast from '@/components/notification/NotificationToast.vue'

const toastRef = ref<InstanceType<typeof NotificationToast> | null>(null)

// 全局提供 toast 方法
provide('toast', {
  success: (title: string, message?: string) => toastRef.value?.success(title, message),
  warning: (title: string, message?: string) => toastRef.value?.warning(title, message),
  error: (title: string, message?: string) => toastRef.value?.error(title, message),
  info: (title: string, message?: string) => toastRef.value?.info(title, message),
})
</script>
