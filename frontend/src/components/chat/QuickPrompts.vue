<template>
  <div class="quick-prompts">
    <span class="prompts-label">快速开始：</span>
    <div class="prompts-scroll">
      <button v-for="p in prompts" :key="p" class="prompt-chip" @click="$emit('select', p)">{{ p }}</button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineEmits<{ select: [prompt: string] }>()
const prompts = ['周末两天去哪里玩？', '带爸妈去北京4天', '蜜月旅行推荐', '一个人去云南发呆', '成都美食之旅', '亲子游推荐']
</script>

<style scoped lang="scss">
$bg-deep: #0a0e1a;
$bg-elevated: #1a2235;
$brand-amber: #f59e0b;
$text-secondary: #94a3b8;
$text-muted: #64748b;
$border: #1e293b;

.quick-prompts {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 20px; overflow: hidden;
  border-top: 1px solid $border;
}

.prompts-label { font-size: 12px; color: $text-muted; white-space: nowrap; flex-shrink: 0; }

.prompts-scroll { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 4px; &::-webkit-scrollbar { display: none; } }

.prompt-chip {
  padding: 6px 14px; background: $bg-elevated; border: 1px solid $border;
  border-radius: 20px; font-size: 12px; color: $text-secondary;
  cursor: pointer; white-space: nowrap; font-family: inherit;
  transition: all 0.25s ease;
  &:hover { border-color: $brand-amber; color: $brand-amber; background: rgba(245,158,11,0.06); }
}
</style>
