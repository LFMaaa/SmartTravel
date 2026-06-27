<template>
  <div class="activity-card" :class="`activity--${activity.type}`">
    <div class="activity-left">
      <div class="type-indicator" :class="activity.type">
        <el-icon :size="14">
          <LocationFilled v-if="activity.type === 'attraction'" />
          <Food v-else-if="activity.type === 'restaurant'" />
          <House v-else-if="activity.type === 'hotel'" />
          <Van v-else />
        </el-icon>
      </div>
      <div class="time-badge" v-if="activity.start_time">
        {{ activity.start_time }}
      </div>
    </div>
    <div class="activity-body">
      <div class="activity-header">
        <span class="activity-name">{{ activity.name }}</span>
        <span class="activity-price" :class="{ free: !activity.price }">
          {{ activity.price > 0 ? `¥${activity.price}` : '免费' }}
        </span>
      </div>
      <div class="activity-meta" v-if="activity.address">
        <el-icon :size="12"><Location /></el-icon>
        <span>{{ activity.address }}</span>
      </div>
      <div class="activity-tags" v-if="activity.tags?.length">
        <el-tag
          v-for="tag in activity.tags"
          :key="tag"
          size="small"
          round
          class="tag"
        >
          {{ tag }}
        </el-tag>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ActivityItem } from '@/types/itinerary'
import { LocationFilled, Food, House, Van, Location } from '@element-plus/icons-vue'

defineProps<{ activity: ActivityItem }>()
</script>

<style scoped lang="scss">
.activity-card {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-md);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
  border-left: 4px solid var(--color-border);
  transition: all var(--transition-base);

  &:hover {
    box-shadow: var(--shadow-md);
    transform: translateX(4px);
  }

  &--attraction { border-left-color: var(--color-secondary); }
  &--restaurant { border-left-color: var(--color-accent); }
  &--hotel { border-left-color: var(--color-primary); }
  &--transport { border-left-color: var(--color-info); }
}

.activity-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-xs);
  flex-shrink: 0;
  min-width: 44px;
}

.type-indicator {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;

  &.attraction { background: var(--color-secondary); }
  &.restaurant { background: var(--color-accent); }
  &.hotel { background: var(--color-primary); }
  &.transport { background: var(--color-info); }
}

.time-badge {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-muted);
  white-space: nowrap;
}

.activity-body {
  flex: 1;
  min-width: 0;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: var(--space-sm);
  margin-bottom: 4px;
}

.activity-name {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
}

.activity-price {
  font-size: var(--font-size-sm);
  font-weight: 700;
  color: var(--color-primary);
  white-space: nowrap;

  &.free {
    color: var(--color-success);
  }
}

.activity-meta {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  margin-bottom: 6px;
}

.activity-tags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;

  .tag {
    font-size: 11px;
  }
}
</style>
