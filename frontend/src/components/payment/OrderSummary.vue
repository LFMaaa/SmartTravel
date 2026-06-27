<template>
  <el-card class="order-summary">
    <template #header>订单摘要</template>
    <div class="summary-row">
      <span>订单编号</span>
      <span>{{ order.id }}</span>
    </div>
    <div class="summary-row">
      <span>订单状态</span>
      <el-tag :type="statusType">{{ order.status }}</el-tag>
    </div>
    <div class="summary-row">
      <span>总金额</span>
      <span class="price">¥{{ order.total_amount }}</span>
    </div>
    <div class="summary-row" v-if="order.expire_at">
      <span>剩余时间</span>
      <CountdownTimer :remaining="remaining" />
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Order } from '@/types/payment'
import CountdownTimer from './CountdownTimer.vue'

const props = defineProps<{ order: Order }>()

const statusType = computed(() => {
  const map: Record<string, string> = { pending: 'warning', paid: 'success', timeout: 'info', cancelled: 'danger' }
  return map[props.order.status] || 'info'
})

const remaining = computed(() => {
  if (!props.order.expire_at) return 0
  return Math.max(0, props.order.expire_at - Math.floor(Date.now() / 1000))
})
</script>

<style scoped>
.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}
.price { color: #f56c6c; font-weight: 600; }
</style>