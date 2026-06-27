<template>
  <div class="countdown-timer">
    <el-icon><Clock /></el-icon>
    <span :class="{ 'timeout': remaining === 0 }">
      {{ formatTime }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ remaining: number }>()

const formatTime = computed(() => {
  const total = props.remaining
  if (!isFinite(total) || total <= 0) return '00:00'
  const m = Math.floor(total / 60)
  const s = total % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
})
</script>

<style scoped>
.countdown-timer {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 16px;
  font-weight: 600;
  color: #409eff;
}
.timeout { color: #f56c6c; }
</style>