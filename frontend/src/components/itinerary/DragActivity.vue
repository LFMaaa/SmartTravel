<template>
  <div class="drag-activity-wrapper" :class="{ 'is-dragging': dragging }">
    <div class="drag-handle" title="拖拽调整顺序">
      <svg viewBox="0 0 16 16" fill="currentColor" width="16" height="16"><circle cx="5" cy="4" r="1.5"/><circle cx="11" cy="4" r="1.5"/><circle cx="5" cy="8" r="1.5"/><circle cx="11" cy="8" r="1.5"/><circle cx="5" cy="12" r="1.5"/><circle cx="11" cy="12" r="1.5"/></svg>
    </div>
    <div class="drag-content">
      <ActivityCard :activity="activity" />
      <div class="activity-actions">
        <el-button text size="small" type="primary" @click.stop="$emit('edit', activity)" title="编辑">
          <el-icon><Edit /></el-icon>
        </el-button>
        <el-button text size="small" type="warning" @click.stop="$emit('replace', activity)" title="替换">
          <el-icon><Switch /></el-icon>
        </el-button>
        <el-button text size="small" type="danger" @click.stop="$emit('delete', activity)" title="删除">
          <el-icon><Delete /></el-icon>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { ActivityItem } from '@/types/itinerary'
import ActivityCard from './ActivityCard.vue'
import { Edit, Switch, Delete } from '@element-plus/icons-vue'

defineProps<{
  activity: ActivityItem
}>()

defineEmits<{
  edit: [activity: ActivityItem]
  replace: [activity: ActivityItem]
  delete: [activity: ActivityItem]
}>()

const dragging = ref(false)
</script>

<style scoped lang="scss">
.drag-activity-wrapper {
  display: flex;
  align-items: stretch;
  gap: 0;
  margin-bottom: var(--space-sm);
  position: relative;
  transition: opacity 0.2s ease;

  &:hover .drag-handle {
    opacity: 1;
  }

  // SortableJS states
  &.sortable-chosen {
    opacity: 0.5;
  }

  &.sortable-drag {
    opacity: 0 !important;
  }

  &.sortable-ghost {
    opacity: 0.4;
    
    .drag-content {
      border: 2px dashed rgba(245, 158, 11, 0.4);
      border-radius: 10px;
      background: rgba(245, 158, 11, 0.05);
    }
  }
}

.drag-handle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  flex-shrink: 0;
  cursor: grab;
  color: var(--color-text-muted);
  opacity: 0;
  transition: opacity var(--transition-base);
  border-radius: var(--radius-sm) 0 0 var(--radius-sm);
  background: var(--color-bg);
  user-select: none;

  &:active {
    cursor: grabbing;
  }

  svg {
    display: block;
  }
}

.drag-content {
  flex: 1;
  min-width: 0;
  position: relative;
  transition: transform var(--transition-base), box-shadow var(--transition-base);
  background: inherit;
  border-radius: 10px;
}

.activity-actions {
  display: flex;
  gap: 2px;
  padding: 0 var(--space-sm) var(--space-sm);
  opacity: 0;
  transition: opacity var(--transition-base);

  .drag-content:hover & {
    opacity: 1;
  }
}
</style>
