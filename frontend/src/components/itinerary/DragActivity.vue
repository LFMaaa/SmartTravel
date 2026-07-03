<template>
  <div class="drag-activity-wrapper" :class="{ 'is-dragging': dragging }">
    <!-- 极简拖拽手柄 -->
    <div class="drag-handle" title="拖拽调整顺序">
      <svg viewBox="0 0 4 16" fill="currentColor" width="4" height="16"><rect width="4" height="16" rx="2"/></svg>
    </div>
    <div class="drag-content">
      <ActivityCard :activity="activity" />
      <!-- 内嵌式操作行 -->
      <div class="activity-actions">
        <button class="act-btn act-edit" @click.stop="$emit('edit', activity)" title="编辑">
          <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.6" width="13" height="13"><path d="M12.5 2.5l3 3L7 14H4v-3l8.5-8.5z"/><path d="M10.5 4.5l3 3"/></svg>
        </button>
        <button class="act-btn act-replace" @click.stop="$emit('replace', activity)" title="AI 替换">
          <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.6" width="13" height="13"><path d="M5 11h3l3-7h2"/><circle cx="13" cy="11" r="2"/><circle cx="5" cy="11" r="2"/></svg>
        </button>
        <button class="act-btn act-del" @click.stop="$emit('delete', activity)" title="删除">
          <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.6" width="13" height="13"><path d="M3 5h12M7 5V3h4v2M5 5v9a1 1 0 001 1h6a1 1 0 001-1V5"/><line x1="8" y1="9" x2="8" y2="13"/><line x1="10" y1="9" x2="10" y2="13"/></svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { ActivityItem } from '@/types/itinerary'
import ActivityCard from './ActivityCard.vue'

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
  border-radius: 10px;
  transition: all 0.25s ease;

  &:hover {
    .drag-handle { opacity: 0.35; }
    .activity-actions { opacity: 1; transform: translateY(0); }
  }

  // SortableJS states
  &.sortable-chosen {
    opacity: 0.55;
    box-shadow: 0 4px 20px rgba(166, 139, 122, 0.15);

    .drag-handle { opacity: 0.7 !important; }
  }

  &.sortable-drag {
    opacity: 0 !important;
  }

  &.sortable-ghost {
    opacity: 0.35;

    .drag-content {
      border: 2px dashed rgba(245, 158, 11, 0.4) !important;
      border-radius: 10px;
      background: rgba(245, 158, 11, 0.04) !important;
    }
  }
}

// ── 拖拽手柄：极细圆角竖条 ──
.drag-handle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 6px;
  flex-shrink: 0;
  cursor: grab;
  color: var(--color-text-muted);
  opacity: 0;
  transition: opacity 0.25s ease, color 0.2s ease;
  user-select: none;

  &:hover,
  &:active {
    opacity: 0.65 !important;
    color: var(--color-primary);
  }

  &:active { cursor: grabbing; }

  svg {
    display: block;
    opacity: 0.45;
    transition: opacity 0.2s;
  }

  &:hover svg { opacity: 1; }
}

// ── 内容区 ──
.drag-content {
  flex: 1;
  min-width: 0;
  position: relative;
  background: inherit;
  border-radius: 0 10px 10px 0;
  overflow: hidden;
}

// ── 操作按钮行：底部内嵌 ──
.activity-actions {
  display: flex;
  justify-content: flex-end;
  gap: 2px;
  padding: 6px 12px 8px;
  opacity: 0;
  transform: translateY(-4px);
  transition: all 0.22s ease;
  pointer-events: none; // 默认不拦截事件

  // hover 时恢复交互
  .drag-content:hover & { pointer-events: auto; }
}

.act-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.2s ease;

  svg {
    flex-shrink: 0;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  // 编辑 — 大地绿
  &.act-edit {
    background: transparent;
    color: var(--color-text-muted);

    &:hover {
      background: rgba(134, 152, 124, 0.12);
      color: var(--color-sage);
    }
  }

  // AI替换 — 主色棕
  &.act-replace {
    background: transparent;
    color: var(--color-text-muted);

    &:hover {
      background: var(--color-primary-lighter);
      color: var(--color-primary);
    }
  }

  // 删除 — 柔和红
  &.act-del {
    background: transparent;
    color: var(--color-text-muted);

    &:hover {
      background: rgba(201, 146, 146, 0.12);
      color: #c99292;
    }
  }

  &:active { transform: scale(0.88); }
}
</style>
