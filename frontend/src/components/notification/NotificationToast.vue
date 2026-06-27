<template>
  <Teleport to="body">
    <transition-group
      name="toast-list"
      tag="div"
      class="notification-toast-container"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast-item', toast.type]"
        @click="remove(toast.id)"
      >
        <div class="toast-icon">
          <el-icon :size="18">
            <CircleCheckFilled v-if="toast.type === 'success'" />
            <WarningFilled v-else-if="toast.type === 'warning'" />
            <CircleCloseFilled v-else-if="toast.type === 'error'" />
            <InfoFilled v-else />
          </el-icon>
        </div>
        <div class="toast-content">
          <div class="toast-title">{{ toast.title }}</div>
          <div v-if="toast.message" class="toast-message">{{ toast.message }}</div>
        </div>
        <button class="toast-close" @click.stop="remove(toast.id)">
          <el-icon :size="14"><Close /></el-icon>
        </button>
      </div>
    </transition-group>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  CircleCheckFilled, WarningFilled, CircleCloseFilled, InfoFilled, Close,
} from '@element-plus/icons-vue'

interface Toast {
  id: number
  type: 'success' | 'warning' | 'error' | 'info'
  title: string
  message?: string
  duration?: number
}

const toasts = ref<Toast[]>([])
let nextId = 0

function add(toast: Omit<Toast, 'id'>) {
  const id = ++nextId
  const item: Toast = { ...toast, id, duration: toast.duration ?? 4000 }
  toasts.value.push(item)

  if (item.duration! > 0) {
    setTimeout(() => remove(id), item.duration)
  }
}

function remove(id: number) {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

function success(title: string, message?: string) {
  add({ type: 'success', title, message })
}

function warning(title: string, message?: string) {
  add({ type: 'warning', title, message })
}

function error(title: string, message?: string) {
  add({ type: 'error', title, message })
}

function info(title: string, message?: string) {
  add({ type: 'info', title, message })
}

defineExpose({ success, warning, error, info, add, remove })
</script>

<style scoped lang="scss">
.notification-toast-container {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 380px;
  pointer-events: none;
}

.toast-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-sm);
  padding: 14px 16px;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  border-left: 4px solid;
  cursor: pointer;
  pointer-events: auto;
  min-width: 300px;

  &.success {
    border-left-color: var(--color-success);
    .toast-icon { color: var(--color-success); }
  }
  &.warning {
    border-left-color: var(--color-warning);
    .toast-icon { color: var(--color-warning); }
  }
  &.error {
    border-left-color: var(--color-danger);
    .toast-icon { color: var(--color-danger); }
  }
  &.info {
    border-left-color: var(--color-info);
    .toast-icon { color: var(--color-info); }
  }
}

.toast-icon {
  flex-shrink: 0;
  margin-top: 1px;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
}

.toast-message {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-top: 2px;
}

.toast-close {
  flex-shrink: 0;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text-muted);
  padding: 2px;
  border-radius: 4px;
  transition: all var(--transition-fast);

  &:hover {
    background: var(--color-bg);
    color: var(--color-text-primary);
  }
}

// Transition
.toast-list-enter-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.toast-list-leave-active {
  transition: all 0.2s ease;
}
.toast-list-enter-from {
  opacity: 0;
  transform: translateX(40px);
}
.toast-list-leave-to {
  opacity: 0;
  transform: translateX(40px);
}
</style>
