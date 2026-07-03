<template>
  <div :class="['chat-message', role]">
    <div v-if="role === 'assistant'" class="message-avatar">
      <div class="ai-avatar">
        <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/></svg>
      </div>
    </div>
    <div class="message-bubble" :class="role"><slot /></div>
    <div v-if="role === 'user'" class="message-avatar">
      <div class="user-avatar">
        <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/></svg>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ role: 'user' | 'assistant' }>()
</script>

<style scoped lang="scss">
$bg-oat: #1a2235;
$brand-brown: #f59e0b;
$brand-brown-light: #fbbf24;
$text-primary: #f1f5f9;
$border: #1e293b;

.chat-message {
  display: flex; gap: 10px; align-items: flex-start; margin-bottom: 16px;
  &.user { justify-content: flex-end; }
}

.message-avatar { flex-shrink: 0; }

.ai-avatar, .user-avatar {
  width: 32px; height: 32px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}

.ai-avatar { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: #0f172a; }
.user-avatar { background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: #fff; }

.message-bubble {
  max-width: 78%; padding: 12px 16px; border-radius: 14px;
  font-size: 13px; line-height: 1.6;
  animation: bounce-in 0.35s ease;

  &.user {
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    color: #0f172a; border-bottom-right-radius: 4px;
  }
  &.assistant {
    background: $bg-oat; color: $text-primary;
    border: 1px solid $border; border-bottom-left-radius: 4px;
  }
}

@keyframes bounce-in {
  0% { opacity: 0; transform: translateY(8px); }
  100% { opacity: 1; transform: translateY(0); }
}
</style>
