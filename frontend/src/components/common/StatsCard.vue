<template>
  <div class="stats-card" :class="[variantClass, { 'card-lift': lift }]">
    <div class="stats-icon" v-if="iconSvg" v-html="iconSvg"></div>
    <div class="stats-value">
      <span class="value-number">{{ formattedValue }}</span>
      <span v-if="suffix" class="value-suffix">{{ suffix }}</span>
    </div>
    <div class="stats-label">{{ label }}</div>
    <div v-if="trend !== undefined" class="stats-trend" :class="{ 'trend-up': trend > 0, 'trend-down': trend < 0 }">
      <svg viewBox="0 0 16 16" fill="currentColor" style="width:14px;height:14px;flex-shrink:0">
        <path v-if="trend > 0" d="M8 4l5 5H3z"/>
        <path v-else-if="trend < 0" d="M8 12l5-5H3z"/>
        <rect v-else x="3" y="7" width="10" height="2" rx="1"/>
      </svg>
      <span>{{ Math.abs(trend) }}%</span>
      <span class="trend-label">较上月</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  icon?: string
  value: number | string
  suffix?: string
  label: string
  variant?: 'primary' | 'secondary' | 'accent'
  trend?: number
  lift?: boolean
}>(), {
  variant: 'primary',
  lift: true,
})

const variantClass = computed(() => `stats-card--${props.variant}`)

const formattedValue = computed(() => {
  if (typeof props.value === 'number') {
    return props.value.toLocaleString()
  }
  return props.value
})

// 内置 SVG 图标映射 — 替代 Element Plus 图标，避免渲染问题
const iconSvgs: Record<string, string> = {
  MapLocation: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>`,
  Money: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>`,
  Clock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
  StarFilled: `<svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>`,
  UserFilled: `<svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
  Ticket: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12V8H4v4a2 2 0 010 4v4h16v-4a2 2 0 010-4z"/><path d="M10 12h4"/></svg>`,
}

const iconSvg = computed(() => {
  if (!props.icon) return null
  const svg = iconSvgs[props.icon]
  return svg || null
})
</script>

<style scoped lang="scss">
.stats-card {
  padding: var(--space-lg);
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
  }

  &--primary::before { background: var(--gradient-hero); }
  &--secondary::before { background: var(--gradient-card); }
  &--accent::before { background: linear-gradient(135deg, #F7A800, #FFC940); }
}

.stats-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-md);

  :deep(svg) {
    width: 22px;
    height: 22px;
  }
}

.stats-card--primary .stats-icon {
  background: rgba(59, 130, 246, 0.12);
  color: #3b82f6;
}

.stats-card--secondary .stats-icon {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
}

.stats-card--accent .stats-icon {
  background: rgba(245, 158, 11, 0.12);
  color: #f59e0b;
}

.stats-value {
  margin-bottom: var(--space-xs);
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.value-number {
  font-size: var(--font-size-2xl);
  font-weight: 800;
  color: var(--color-text-primary);
}

.value-suffix {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.stats-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.stats-trend {
  margin-top: var(--space-sm);
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
  font-weight: 600;

  &.trend-up { color: var(--color-success); }
  &.trend-down { color: var(--color-danger); }

  .trend-label {
    font-weight: 400;
    color: var(--color-text-muted);
    margin-left: 2px;
  }
}
</style>
