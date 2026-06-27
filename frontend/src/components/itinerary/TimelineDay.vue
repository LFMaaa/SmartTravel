<template>
  <div class="timeline-day">
    <div class="day-header">
      <div class="day-title-row">
        <span class="day-number">Day {{ day.day_index }}</span>
        <span v-if="day.date" class="day-date">{{ day.date }}</span>
        <el-tag size="small" round>{{ day.activities?.length || 0 }} 个活动</el-tag>
      </div>
    </div>

    <div class="timeline-track">
      <div
        v-for="(activity, index) in day.activities"
        :key="activity.id || index"
        class="timeline-item"
      >
        <div class="timeline-node">
          <div class="node-dot" :class="activity.type" />
          <div v-if="index < (day.activities?.length || 0) - 1" class="node-line" />
        </div>
        <div class="timeline-content">
          <ActivityCard :activity="activity" />
        </div>
      </div>

      <!-- Hotel section -->
      <div v-if="day.hotel" class="timeline-item hotel-item">
        <div class="timeline-node">
          <div class="node-dot hotel" />
        </div>
        <div class="timeline-content">
          <div class="hotel-label">
            <el-icon :size="14"><Moon /></el-icon>
            <span>住宿</span>
          </div>
          <ActivityCard :activity="day.hotel" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DayItinerary } from '@/types/itinerary'
import ActivityCard from './ActivityCard.vue'
import { Moon } from '@element-plus/icons-vue'

defineProps<{ day: DayItinerary }>()
</script>

<style scoped lang="scss">
.timeline-day {
  padding: var(--space-md);
}

.day-header {
  margin-bottom: var(--space-md);
}

.day-title-row {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.day-number {
  font-size: var(--font-size-lg);
  font-weight: 800;
  color: var(--color-text-primary);
}

.day-date {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.timeline-track {
  position: relative;
}

.timeline-item {
  display: flex;
  gap: var(--space-md);
}

.timeline-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
  width: 20px;
}

.node-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 3px solid var(--color-border);
  background: var(--color-surface);
  flex-shrink: 0;

  &.attraction { border-color: var(--color-secondary); background: var(--color-secondary-lighter); }
  &.restaurant { border-color: var(--color-accent); background: var(--color-accent-lighter); }
  &.transport { border-color: var(--color-info); background: var(--color-info-light); }
  &.hotel { border-color: var(--color-primary); background: var(--color-primary-lighter); }
}

.node-line {
  width: 2px;
  flex: 1;
  min-height: 16px;
  background: var(--color-border-light);
  margin: 4px 0;
}

.timeline-content {
  flex: 1;
  min-width: 0;
  padding-bottom: var(--space-md);
}

.hotel-item {
  .timeline-content {
    padding-top: var(--space-sm);
    border-top: 1px dashed var(--color-border-light);
  }
}

.hotel-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--color-primary);
  margin-bottom: var(--space-sm);
}
</style>
