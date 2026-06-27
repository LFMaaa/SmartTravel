<template>
  <div class="day-navigator">
    <button
      v-for="(day, index) in days"
      :key="day.day_index"
      :class="['day-tab', { active: modelValue === index }]"
      @click="$emit('update:modelValue', index)"
    >
      <span class="day-label">Day {{ day.day_index }}</span>
      <span v-if="day.date" class="day-date">{{ formatDate(day.date) }}</span>
      <span class="day-badge">{{ day.activities?.length || 0 }}</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import type { DayItinerary } from '@/types/itinerary'

defineProps<{
  days: DayItinerary[]
  modelValue: number
}>()

defineEmits<{ 'update:modelValue': [index: number] }>()

function formatDate(dateStr: string) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getMonth() + 1}/${d.getDate()}`
}
</script>

<style scoped lang="scss">
.day-navigator {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 4px 0 var(--space-sm);
  border-bottom: 1px solid var(--color-border-light);
  margin-bottom: var(--space-md);

  &::-webkit-scrollbar { display: none; }
}

.day-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  min-width: 72px;
  padding: var(--space-sm) var(--space-md);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  cursor: pointer;
  font-family: var(--font-family);
  transition: all var(--transition-base);

  &:hover {
    border-color: var(--color-primary);
  }

  &.active {
    border-color: var(--color-primary);
    background: var(--color-primary-lighter);

    .day-label { color: var(--color-primary); }
    .day-badge { background: var(--color-primary); color: #fff; }
  }
}

.day-label {
  font-size: var(--font-size-xs);
  font-weight: 700;
  color: var(--color-text-primary);
}

.day-date {
  font-size: 10px;
  color: var(--color-text-muted);
}

.day-badge {
  margin-top: 2px;
  min-width: 20px;
  height: 20px;
  border-radius: 10px;
  background: var(--color-bg);
  color: var(--color-text-secondary);
  font-size: 11px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 6px;
}
</style>
