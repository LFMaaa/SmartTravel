<template>
  <div class="editor-page-wrapper">
    <!-- Top accent line -->
    <div class="editor-accent-bar"></div>

    <!-- Header -->
    <div class="editor-header">
      <button class="back-btn" @click="handleBack">
        <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd"/></svg>
        <span>返回 AI 规划</span>
      </button>

      <div class="header-center">
        <span class="editor-title">行程编辑器</span>
        <span class="editor-subtitle">拖拽排序 · 点击编辑 · 自由调整行程</span>
      </div>

      <div class="editor-actions">
        <slot name="actions" />
      </div>
    </div>

    <!-- Body -->
    <div class="editor-body">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function handleBack() {
  router.push('/itinerary/generate')
}
</script>

<style scoped lang="scss">
.editor-page-wrapper {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg);
}

.editor-accent-bar {
  height: 3px;
  background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-nude-pink) 40%, var(--color-sage) 100%);
  flex-shrink: 0;
  opacity: 0.85;
}

.editor-header {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: 0 var(--space-lg);
  height: 56px;
  background: linear-gradient(180deg, #FFFFFF 0%, var(--color-bg) 100%);
  border-bottom: 1px solid var(--color-border-light);
  flex-shrink: 0;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  background: var(--color-surface);
  color: var(--color-text-secondary);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.22s ease;
  flex-shrink: 0;

  svg { flex-shrink: 0; opacity: 0.7; transition: transform 0.22s ease; }

  &:hover {
    color: var(--color-primary);
    background: var(--color-bg-alt);
    border-color: var(--color-primary-light);

    svg {
      opacity: 1;
      transform: translateX(-2px);
    }
  }

  &:active { transform: scale(0.96); }
}

.header-center {
  flex: 1;
  display: flex;
  align-items: baseline;
  gap: var(--space-md);
  min-width: 0;
}

.editor-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: 0.3px;
}

.editor-subtitle {
  font-size: 11px;
  color: var(--color-text-muted);
  letter-spacing: 0.2px;
  white-space: nowrap;
}

.editor-actions {
  display: flex;
  gap: var(--space-sm);
  flex-shrink: 0;
}

.editor-body {
  flex: 1;
  overflow: auto;
}
</style>
