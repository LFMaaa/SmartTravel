<template>
  <div class="generate-view">
    <div class="generate-panel">
      <!-- Left: Chat Section -->
      <div class="chat-section">
        <ChatPanel :query="route.query.q as string" @generated="onGenerated" />
      </div>

      <!-- Right: Preview Section -->
      <div class="preview-section">
        <ItineraryPreview v-if="itinerary" :itinerary="itinerary" />

        <div v-else class="preview-empty">
          <div class="empty-animation">
            <div class="orbit-ring">
              <div class="orbit-dot dot-1"></div>
              <div class="orbit-dot dot-2"></div>
              <div class="orbit-dot dot-3"></div>
            </div>
            <div class="center-icon">🤖</div>
          </div>

          <h3>AI 行程规划助手</h3>
          <p>在左侧描述你的旅行需求，AI 将为你实时生成专属行程方案</p>

          <div class="empty-hints">
            <div v-for="h in hints" :key="h.label" class="hint-item">
              <div class="hint-icon">{{ h.emoji }}</div>
              <span>{{ h.label }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useItineraryStore } from '@/stores/itinerary'
import ChatPanel from '@/components/chat/ChatPanel.vue'
import ItineraryPreview from '@/components/itinerary/ItineraryPreview.vue'
import type { ItineraryResponse } from '@/types/itinerary'

const route = useRoute()
const itineraryStore = useItineraryStore()
const itinerary = ref<ItineraryResponse | null>(null)

function onGenerated(result: ItineraryResponse) { itinerary.value = result }

onMounted(() => {
  const stored = itineraryStore.currentItinerary
  if (stored && stored.days && stored.days.length > 0) {
    itinerary.value = stored
  }
})

const hints = [
  { emoji: '💬', label: '自然语言描述需求' },
  { emoji: '⚡', label: '实时流式生成' },
  { emoji: '✏️', label: '自由调整编辑' },
]
</script>

<style scoped lang="scss">
$bg-warm: #FAF8F3;
$bg-oat: #F5F0E8;
$bg-white: #FFFFFF;
$brand-brown: #A68B7A;
$brand-nude: #E8D5D0;
$brand-sage: #B8C4B8;
$text-primary: #3D3D3D;
$text-secondary: #6B6B6B;
$text-muted: #B8B0A8;
$border: #E8D5D0;

.generate-view {
  height: 100vh;
  padding: 20px;
  background: $bg-warm;
}

.generate-panel {
  display: flex;
  gap: 20px;
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.chat-section {
  flex: 1;
  min-width: 0;
  max-width: 460px;
  background: $bg-white;
  border-radius: 20px;
  border: 1px solid $border;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(166, 139, 122, 0.06);
}

.preview-section {
  flex: 1.2;
  min-width: 0;
  background: $bg-white;
  border-radius: 20px;
  border: 1px solid $border;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(166, 139, 122, 0.06);
}

.preview-empty {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 40px;
  text-align: center;
}

.empty-animation {
  position: relative;
  width: 160px;
  height: 160px;
  margin-bottom: 36px;
}

.orbit-ring {
  position: absolute;
  inset: 0;
  border: 2px dashed rgba(184, 196, 184, 0.3);
  border-radius: 50%;
  animation: rotate 20s linear infinite;

  .orbit-dot {
    position: absolute;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: linear-gradient(135deg, #E8D5D0, #B8C4B8);

    &.dot-1 { top: -5px; left: 50%; transform: translateX(-50%); }
    &.dot-2 { bottom: 22%; right: -5px; }
    &.dot-3 { bottom: 22%; left: -5px; }
  }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.center-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 68px;
  height: 68px;
  background: linear-gradient(135deg, #E8D5D0, #B8C4B8);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  box-shadow: 0 12px 32px rgba(184, 196, 184, 0.35);
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.05); }
}

.preview-empty h3 {
  font-size: 22px;
  font-weight: 600;
  color: $text-primary;
  margin-bottom: 10px;
}

.preview-empty > p {
  font-size: 14px;
  color: $text-muted;
  max-width: 300px;
  line-height: 1.6;
  margin-bottom: 40px;
}

.empty-hints {
  display: flex;
  gap: 36px;
}

.hint-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: $text-muted;

  .hint-icon {
    width: 48px;
    height: 48px;
    background: $bg-oat;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    border: 1px solid $border;
    transition: all 0.3s ease;
  }

  &:hover .hint-icon {
    background: linear-gradient(135deg, #E8D5D0, #B8C4B8);
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(184, 196, 184, 0.35);
  }
}

@media (max-width: 768px) {
  .generate-view { padding: 12px; height: auto; }
  .generate-panel { flex-direction: column; height: auto; }
  .chat-section { max-width: none; height: 500px; }
  .preview-section { height: 500px; }
}
</style>
