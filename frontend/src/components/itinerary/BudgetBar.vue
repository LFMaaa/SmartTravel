<template>
  <div class="budget-bar" v-if="total > 0">
    <div class="budget-header">
      <span class="budget-label">预算分配</span>
      <span class="budget-total">¥{{ total.toLocaleString() }}</span>
    </div>
    <div class="bar-track">
      <div
        v-for="segment in segments"
        :key="segment.type"
        class="bar-segment"
        :style="{
          width: segment.percent + '%',
          background: segment.color,
        }"
        :title="`${segment.label}: ¥${segment.amount} (${segment.percent}%)`"
      />
    </div>
    <div class="budget-legend">
      <div v-for="segment in segments" :key="segment.type" class="legend-item">
        <span class="legend-dot" :style="{ background: segment.color }" />
        <span class="legend-label">{{ segment.label }}</span>
        <span class="legend-amount">¥{{ segment.amount }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { DayItinerary, ActivityItem } from '@/types/itinerary'

const props = defineProps<{
  days: DayItinerary[]
}>()

const colors: Record<string, string> = {
  hotel: '#FF6B35',
  attraction: '#0D7377',
  restaurant: '#F7A800',
  transport: '#74B9FF',
}

const labels: Record<string, string> = {
  hotel: '住宿',
  attraction: '景点',
  restaurant: '餐饮',
  transport: '交通',
}

// Dify 工作流可能返回中文 type 值，做标准化映射
function normalizeType(raw: string): string {
  const map: Record<string, string> = {
    '酒店': 'hotel', '住宿': 'hotel',
    '景点': 'attraction', '景区': 'attraction',
    '餐厅': 'restaurant', '餐饮': 'restaurant', '美食': 'restaurant',
    '交通': 'transport',
  }
  return map[raw] || raw
}

const total = computed(() => {
  if (!props.days) return 0
  let sum = 0
  for (const day of props.days) {
    for (const act of day.activities || []) {
      sum += act.price || 0
    }
    if (day.hotel) sum += day.hotel.price || 0
  }
  return sum
})

const segments = computed(() => {
  const groups: Record<string, number> = { hotel: 0, attraction: 0, restaurant: 0, transport: 0 }
  if (!props.days) return []
  for (const day of props.days) {
    for (const act of day.activities || []) {
      const type = normalizeType(act.type || 'attraction')
      if (groups[type] !== undefined) groups[type] += act.price || 0
    }
    if (day.hotel) groups.hotel += day.hotel.price || 0
  }
  const t = total.value || 1
  return Object.entries(groups)
    .filter(([, v]) => v > 0)
    .map(([type, amount]) => ({
      type,
      amount,
      label: labels[type] || type,
      color: colors[type] || '#B2BEC3',
      percent: Math.round((amount / t) * 100),
    }))
})
</script>

<style scoped lang="scss">
.budget-bar {
  padding: var(--space-md);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
  margin-bottom: var(--space-md);
}

.budget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-sm);
}

.budget-label {
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.budget-total {
  font-size: var(--font-size-lg);
  font-weight: 800;
  color: var(--color-primary);
}

.bar-track {
  height: 8px;
  background: var(--color-border-light);
  border-radius: 4px;
  overflow: hidden;
  display: flex;
  margin-bottom: var(--space-sm);
}

.bar-segment {
  height: 100%;
  transition: width var(--transition-slow);

  &:first-child { border-radius: 4px 0 0 4px; }
  &:last-child { border-radius: 0 4px 4px 0; }
  &:only-child { border-radius: 4px; }
}

.budget-legend {
  display: flex;
  gap: var(--space-md);
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.legend-label {
  color: var(--color-text-secondary);
}

.legend-amount {
  color: var(--color-text-primary);
  font-weight: 600;
}
</style>
