<template>
  <div class="resource-lock" :class="{ warning: isWarning, expired: remaining <= 0 }">
    <div class="lock-icon">
      <el-icon :size="20" v-if="remaining > 0"><Lock /></el-icon>
      <el-icon :size="20" v-else><Unlock /></el-icon>
    </div>
    <div class="lock-info">
      <div class="lock-title" v-if="remaining > 0">资源已锁定</div>
      <div class="lock-title expired-title" v-else>资源已释放</div>
      <div class="lock-timer">{{ formatCountdown }}</div>
    </div>
    <div class="lock-progress">
      <div class="progress-fill" :style="{ width: progressPercent + '%' }" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Lock, Unlock } from '@element-plus/icons-vue'

const props = defineProps<{
  remaining: number
  totalDuration?: number
}>()

const isWarning = computed(() => props.remaining > 0 && props.remaining <= 300)
const progressPercent = computed(() => {
  const total = props.totalDuration || 900
  return Math.max(0, (props.remaining / total) * 100)
})

const formatCountdown = computed(() => {
  const m = Math.floor(props.remaining / 60)
  const s = props.remaining % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
})
</script>

<style scoped lang="scss">
.resource-lock {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md) var(--space-lg);
  background: var(--color-success-light);
  border-radius: var(--radius-md);
  position: relative;
  overflow: hidden;

  &.warning {
    background: var(--color-warning-light);
    .lock-timer { color: var(--color-warning); }
    animation: pulse-scale 2s ease-in-out infinite;
  }

  &.expired {
    background: var(--color-danger-light);
    .lock-timer { color: var(--color-danger); }
  }
}

.lock-icon { color: var(--color-success); flex-shrink: 0; }
.expired .lock-icon { color: var(--color-danger); }

.lock-info { flex: 1; }
.lock-title { font-size: var(--font-size-sm); font-weight: 600; color: var(--color-text-primary); }
.expired-title { color: var(--color-danger); }

.lock-timer {
  font-size: var(--font-size-xl);
  font-weight: 800;
  font-family: monospace;
  color: var(--color-success);
}

.lock-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: rgba(0,0,0,0.05);
}

.progress-fill {
  height: 100%;
  background: var(--color-success);
  transition: width 1s linear;
  .warning & { background: var(--color-warning); }
  .expired & { background: var(--color-danger); width: 0; }
}
</style>
