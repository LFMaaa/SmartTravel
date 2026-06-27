<template>
  <div class="feature-card" :class="[variantClass, { 'card-lift': lift }]">
    <div class="feature-icon" :class="iconBgClass">
      <el-icon :size="iconSize">
        <component :is="icon" />
      </el-icon>
    </div>
    <h3 class="feature-title">{{ title }}</h3>
    <p class="feature-desc">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  icon: any
  title: string
  description: string
  variant?: 'primary' | 'secondary' | 'accent'
  iconSize?: number | string
  lift?: boolean
}>(), {
  variant: 'primary',
  iconSize: 24,
  lift: true,
})

const variantClass = computed(() => `feature-card--${props.variant}`)
const iconBgClass = computed(() => `icon-bg--${props.variant}`)
</script>

<style scoped lang="scss">
.feature-card {
  padding: var(--space-xl);
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  text-align: center;

  &--primary {
    .feature-title { color: var(--color-primary); }
  }
  &--secondary {
    .feature-title { color: var(--color-secondary); }
  }
  &--accent {
    .feature-title { color: var(--color-accent); }
  }
}

.feature-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-lg);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-lg);

  :deep(.el-icon) {
    color: #fff;
  }
}

.icon-bg--primary {
  background: var(--gradient-hero);
}
.icon-bg--secondary {
  background: var(--gradient-card);
}
.icon-bg--accent {
  background: linear-gradient(135deg, #F7A800, #FFC940);
}

.feature-title {
  font-size: var(--font-size-lg);
  font-weight: 700;
  margin-bottom: var(--space-sm);
}

.feature-desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: 1.6;
}
</style>
