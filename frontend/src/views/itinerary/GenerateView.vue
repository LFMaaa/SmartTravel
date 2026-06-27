<template>
  <div class="generate-container">
    <div class="generate-panel">
      <!-- Left: Chat section -->
      <div class="chat-section">
        <ChatPanel :query="route.query.q as string" @generated="onGenerated" />
      </div>

      <!-- Right: Preview section -->
      <div class="preview-section">
        <ItineraryPreview v-if="itinerary" :itinerary="itinerary" />

        <div v-else class="preview-empty">
          <div class="empty-animation">
            <div class="orbit-ring">
              <div class="orbit-dot dot-1"></div>
              <div class="orbit-dot dot-2"></div>
              <div class="orbit-dot dot-3"></div>
            </div>
            <div class="center-icon">
              <svg viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/></svg>
            </div>
          </div>

          <h3>AI 行程规划助手</h3>
          <p>在左侧描述你的旅行需求，AI 将为你实时生成专属行程方案</p>

          <div class="empty-hints">
            <div v-for="h in hints" :key="h.label" class="hint-item">
              <div class="hint-icon">
                <svg viewBox="0 0 20 20" fill="currentColor" width="20" height="20"><path :d="h.path"/></svg>
              </div>
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

// 从编辑器返回时，从 Pinia store 恢复行程数据
onMounted(() => {
  const stored = itineraryStore.currentItinerary
  if (stored && stored.days && stored.days.length > 0) {
    itinerary.value = stored
  }
})

const hints = [
  { label: '自然语言描述需求', path: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z' },
  { label: '实时流式生成', path: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' },
  { label: '自由调整编辑', path: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z' },
]
</script>

<style scoped lang="scss">
$bg-deep: #0a0e1a;
$bg-card: #111827;
$bg-elevated: #1a2235;
$brand-amber: #f59e0b;
$text-primary: #f1f5f9;
$text-secondary: #94a3b8;
$text-muted: #64748b;
$border: #1e293b;

.generate-container {
  height: calc(100vh - 64px);
  padding: 20px;
  background: $bg-deep;
}

.generate-panel {
  display: flex; gap: 20px; height: 100%;
  max-width: 1400px; margin: 0 auto;
}

.chat-section {
  flex: 1; min-width: 0; max-width: 480px;
  background: $bg-card;
  border-radius: 20px;
  border: 1px solid $border;
  overflow: hidden;
}

.preview-section {
  flex: 1.2; min-width: 0;
  background: $bg-card;
  border-radius: 20px;
  border: 1px solid $border;
  overflow: hidden;
}

.preview-empty {
  height: 100%; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 60px 40px; text-align: center;
}

.empty-animation {
  position: relative; width: 180px; height: 180px; margin-bottom: 40px;
}

.orbit-ring {
  position: absolute; inset: 0;
  border: 2px dashed rgba(245, 158, 11, 0.15);
  border-radius: 50%;
  animation: rotate 20s linear infinite;

  .orbit-dot {
    position: absolute; width: 10px; height: 10px; border-radius: 50%;
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
    &.dot-1 { top: -5px; left: 50%; transform: translateX(-50%); }
    &.dot-2 { bottom: 22%; right: -5px; }
    &.dot-3 { bottom: 22%; left: -5px; }
  }
}

@keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.center-icon {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 72px; height: 72px;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  border-radius: 20px;
  display: flex; align-items: center; justify-content: center;
  color: #0f172a;
  box-shadow: 0 12px 32px rgba(245, 158, 11, 0.35);
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.05); }
}

.preview-empty h3 {
  font-size: 22px; font-weight: 700; color: $text-primary; margin-bottom: 10px;
}

.preview-empty > p {
  font-size: 14px; color: $text-muted; max-width: 300px; line-height: 1.6; margin-bottom: 40px;
}

.empty-hints { display: flex; gap: 32px; }

.hint-item {
  display: flex; flex-direction: column; align-items: center; gap: 10px;
  font-size: 12px; color: $text-muted;

  .hint-icon {
    width: 44px; height: 44px;
    background: $bg-elevated;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    color: $brand-amber;
    border: 1px solid $border;
    transition: all 0.3s ease;
  }

  &:hover .hint-icon {
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    color: #0f172a;
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(245, 158, 11, 0.3);
    border-color: transparent;
  }
}

@media (max-width: 768px) {
  .generate-container { padding: 12px; height: auto; }
  .generate-panel { flex-direction: column; height: auto; }
  .chat-section { max-width: none; height: 500px; }
  .preview-section { height: 500px; }
}
</style>
