<template>
  <div class="itinerary-preview">
    <!-- Header -->
    <div class="preview-header">
      <div class="header-top">
        <h3 class="preview-title">{{ itinerary.title }}</h3>
        <el-tag
          :type="statusType"
          size="small"
          round
          effect="dark"
        >
          {{ statusLabel }}
        </el-tag>
      </div>
      <div class="header-meta">
        <div class="meta-item">
          <el-icon :size="16"><LocationFilled /></el-icon>
          <span>{{ itinerary.destination }}</span>
        </div>
        <div class="meta-divider" />
        <div class="meta-item">
          <el-icon :size="16"><Calendar /></el-icon>
          <span>{{ itinerary.days?.length || 0 }} 天行程</span>
        </div>
        <div class="meta-divider" />
        <div class="meta-item price">
          <el-icon :size="16"><Money /></el-icon>
          <span>¥{{ (itinerary.total_budget || 0).toLocaleString() }}</span>
        </div>
      </div>
    </div>

    <!-- Budget bar -->
    <BudgetBar v-if="itinerary.days" :days="itinerary.days" />

    <!-- Day navigator -->
    <DayNavigator
      v-if="itinerary.days && itinerary.days.length > 1"
      v-model="activeDay"
      :days="itinerary.days"
    />

    <!-- Timeline for active day -->
    <div v-if="itinerary.days && itinerary.days[activeDay]" class="preview-timeline">
      <TimelineDay :day="itinerary.days[activeDay]" />
    </div>

    <!-- Action buttons -->
    <div class="preview-actions">
      <button class="action-btn action-btn-edit" @click="$router.push(`/editor/${itinerary.id}`)">
        <svg viewBox="0 0 20 20" fill="currentColor" width="18" height="18"><path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/></svg>
        编辑行程
      </button>
      <button class="action-btn action-btn-view" @click="$router.push(`/itinerary/${itinerary.id}`)">
        <svg viewBox="0 0 20 20" fill="currentColor" width="18" height="18"><path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/><path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/></svg>
        查看详情
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { ItineraryResponse } from '@/types/itinerary'
import TimelineDay from './TimelineDay.vue'
import DayNavigator from './DayNavigator.vue'
import BudgetBar from './BudgetBar.vue'
import { LocationFilled, Calendar, Money } from '@element-plus/icons-vue'

const props = defineProps<{ itinerary: ItineraryResponse }>()

const activeDay = ref(0)

const statusLabel = computed(() => {
  const map: Record<string, string> = {
    draft: '草稿',
    planned: '已规划',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消',
  }
  return map[props.itinerary.status] || props.itinerary.status
})

const statusType = computed(() => {
  const map: Record<string, string> = {
    draft: 'info',
    planned: 'warning',
    in_progress: 'success',
    completed: 'success',
    cancelled: 'danger',
  }
  return map[props.itinerary.status] || 'info'
})
</script>

<style scoped lang="scss">
.itinerary-preview {
  padding: var(--space-lg);
  height: 100%;
  overflow-y: auto;
}

.preview-header {
  margin-bottom: var(--space-lg);
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-md);
  margin-bottom: var(--space-md);
}

.preview-title {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
  flex: 1;
}

.header-meta {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);

  &.price {
    color: var(--color-primary);
    font-weight: 600;
  }
}

.meta-divider {
  width: 1px;
  height: 14px;
  background: var(--color-border);
}

.preview-timeline {
  margin-bottom: var(--space-lg);
}

.preview-actions {
  display: flex;
  gap: var(--space-md);
  padding-top: var(--space-md);
  border-top: 1px solid var(--color-border-light);
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;

  svg { flex-shrink: 0; }
}

.action-btn-edit {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #0f172a;
  box-shadow: 0 4px 14px rgba(245, 158, 11, 0.3);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(245, 158, 11, 0.45);
  }
}

.action-btn-view {
  background: rgba(255,255,255,0.06);
  color: #e2e8f0;
  border: 1px solid rgba(255,255,255,0.12);

  &:hover {
    background: rgba(255,255,255,0.1);
    border-color: rgba(255,255,255,0.2);
    transform: translateY(-2px);
  }
}
</style>
