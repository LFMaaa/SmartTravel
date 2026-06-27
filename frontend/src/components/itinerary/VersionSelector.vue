<template>
  <div class="version-selector">
    <div
      v-for="v in versions"
      :key="v.version"
      class="version-item"
      :class="{ active: v.version === modelValue }"
      @click="$emit('update:modelValue', v.version)"
    >
      <div class="version-dot"></div>
      <div class="version-info">
        <div class="version-top">
          <span class="version-num">v{{ v.version }}</span>
          <span v-if="v.summary" class="version-summary-label">{{ v.summary }}</span>
        </div>
        <div class="version-time" v-if="v.created_at">{{ formatTime(v.created_at) }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface VersionInfo {
  version: number
  created_at: string
  summary?: string
}

defineProps<{
  modelValue: number
  versions: VersionInfo[]
}>()

defineEmits<{ 'update:modelValue': [version: number] }>()

function formatTime(dateStr: string) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const month = d.getMonth() + 1
  const day = d.getDate()
  const hour = String(d.getHours()).padStart(2, '0')
  const min = String(d.getMinutes()).padStart(2, '0')
  return `${month}月${day}日 ${hour}:${min}`
}
</script>

<style scoped lang="scss">
.version-selector {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.version-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;

  &:hover { background: rgba(255,255,255,0.04); }

  &.active {
    background: rgba(245, 158, 11, 0.08);

    .version-dot {
      background: #f59e0b;
      box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2);
    }
    .version-num { color: #f59e0b; }
  }
}

.version-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #475569;
  margin-top: 4px;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.version-info {
  flex: 1;
  min-width: 0;
}

.version-top {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 2px;
}

.version-num {
  font-weight: 700;
  font-size: 13px;
  color: #e2e8f0;
  transition: color 0.2s ease;
}

.version-summary-label {
  font-size: 11px;
  color: #64748b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.version-time {
  font-size: 11px;
  color: #475569;
}
</style>
