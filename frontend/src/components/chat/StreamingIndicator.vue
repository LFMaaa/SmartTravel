<template>
  <div class="streaming-indicator">
    <div class="indicator-content">
      <div class="pulse-dot"></div>
      <span class="indicator-text">{{ text }}</span>
      <span class="typing-dots"><span>.</span><span>.</span><span>.</span></span>
    </div>
    <div class="progress-bar"><div class="progress-fill"></div></div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ text?: string }>(), { text: 'AI 正在为您规划行程' })
</script>

<style scoped lang="scss">
$bg-oat: #1a2235;
$brand-brown: #f59e0b;
$text-primary: #f1f5f9;
$border: #1e293b;

.streaming-indicator {
  padding: 16px; background: $bg-oat;
  border-radius: 14px; border: 1px solid $border; margin-bottom: 16px;
}

.indicator-content {
  display: flex; align-items: center; gap: 10px; margin-bottom: 10px;
}

.pulse-dot {
  width: 10px; height: 10px; border-radius: 50%; background: $brand-brown;
  animation: pulse-glow 1.5s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 4px $brand-brown; }
  50% { box-shadow: 0 0 12px $brand-brown, 0 0 24px rgba(245,158,11,0.3); }
}

.indicator-text { font-size: 13px; font-weight: 500; color: $text-primary; }

.typing-dots {
  color: $brand-brown; font-weight: 700; font-size: 18px;
  span { animation: blink-cursor 1.4s infinite both;
    &:nth-child(2) { animation-delay: 0.2s; }
    &:nth-child(3) { animation-delay: 0.4s; }
  }
}

@keyframes blink-cursor {
  0%, 20% { opacity: 0; }
  50% { opacity: 1; }
  100% { opacity: 0; }
}

.progress-bar { height: 3px; background: $border; border-radius: 2px; overflow: hidden; }
.progress-fill {
  height: 100%; width: 40%;
  background: linear-gradient(90deg, $brand-brown, transparent);
  border-radius: 2px;
  animation: shimmer 1.5s ease-in-out infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(250%); }
}
</style>
