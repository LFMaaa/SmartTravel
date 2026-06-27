<template>
  <div class="booking-item" :class="{ failed: status === 'failed' }">
    <div class="item-main">
      <div class="item-type-badge" :class="resourceType">
        {{ typeLabel }}
      </div>
      <div class="item-info">
        <div class="item-name">{{ name }}</div>
        <div class="item-meta">
          <span v-if="date">{{ date }}</span>
          <span v-if="time"> · {{ time }}</span>
        </div>
      </div>
      <div class="item-price">¥{{ price }}</div>
    </div>
    <div class="item-status">
      <el-tag :type="statusTagType" size="small" round>
        {{ statusLabel }}
      </el-tag>
      <el-button
        v-if="status === 'failed'"
        size="small"
        type="warning"
        text
        @click="$emit('findAlternative')"
      >
        查看备选
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  name: string
  resourceType: 'hotel' | 'ticket' | 'flight' | 'restaurant' | 'insurance'
  price: number
  status: 'pending' | 'locked' | 'failed'
  date?: string
  time?: string
}>()

defineEmits<{ findAlternative: [] }>()

const typeLabel = computed(() => {
  const map: Record<string, string> = { hotel: '酒店', ticket: '门票', flight: '机票', restaurant: '餐厅', insurance: '保险' }
  return map[props.resourceType] || props.resourceType
})

const statusLabel = computed(() => {
  const map: Record<string, string> = { pending: '待预订', locked: '已占位', failed: '预订失败' }
  return map[props.status] || props.status
})

const statusTagType = computed(() => {
  const map: Record<string, string> = { pending: 'info', locked: 'success', failed: 'danger' }
  return map[props.status] || 'info'
})
</script>

<style scoped lang="scss">
.booking-item {
  padding: var(--space-md);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
  margin-bottom: var(--space-sm);
  transition: all var(--transition-base);

  &.failed {
    border-color: var(--color-danger);
    background: var(--color-danger-light);
  }
}

.item-main {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  margin-bottom: var(--space-sm);
}

.item-type-badge {
  font-size: 10px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  &.hotel { background: var(--color-primary-lighter); color: var(--color-primary); }
  &.ticket { background: var(--color-warning-light); color: var(--color-warning); }
  &.flight { background: var(--color-info-light); color: var(--color-info); }
  &.restaurant { background: #E8F5E9; color: var(--color-success); }
}

.item-info { flex: 1; }
.item-name { font-size: var(--font-size-sm); font-weight: 600; color: var(--color-text-primary); }
.item-meta { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.item-price { font-size: var(--font-size-sm); font-weight: 700; color: var(--color-primary); }

.item-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
