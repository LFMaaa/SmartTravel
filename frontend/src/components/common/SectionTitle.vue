<template>
  <div class="section-title" :class="{ 'text-center': centered }">
    <span v-if="overline" class="overline">{{ overline }}</span>
    <h2 :class="['title', sizeClass]"><slot /></h2>
    <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
    <div v-if="!noLine" class="decorative-line" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = withDefaults(defineProps<{
  overline?: string; subtitle?: string; centered?: boolean; size?: 'sm' | 'md' | 'lg'; noLine?: boolean
}>(), { centered: false, size: 'md', noLine: false })
const sizeClass = computed(() => `title--${props.size}`)
</script>

<style scoped lang="scss">
$brand-amber: #f59e0b;
$text-primary: #f1f5f9;
$text-secondary: #94a3b8;

.section-title { margin-bottom: var(--space-xl); }

.overline {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: $brand-amber;
  margin-bottom: var(--space-sm);
  background: rgba(245, 158, 11, 0.08);
  padding: 4px 14px;
  border-radius: var(--radius-full);
  border: 1px solid rgba(245, 158, 11, 0.15);
}

.title {
  font-weight: 700;
  color: $text-primary;
  line-height: 1.3;
  &--sm { font-size: 22px; }
  &--md { font-size: 30px; }
  &--lg { font-size: 38px; }
}

.subtitle {
  margin-top: var(--space-sm);
  font-size: 15px;
  color: $text-secondary;
  line-height: 1.6;
}

.decorative-line {
  width: 48px; height: 3px;
  background: linear-gradient(90deg, $brand-amber, transparent);
  border-radius: 2px;
  margin-top: var(--space-md);
}

.text-center {
  text-align: center;
  .decorative-line { margin-left: auto; margin-right: auto; }
}
</style>
