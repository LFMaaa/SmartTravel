<template>
  <section class="feature-section">
    <div class="container">
      <SectionTitle overline="为什么选择智游" subtitle="不仅仅是行程规划，更是你的 AI 旅行管家" centered>
        AI 让旅行更简单
      </SectionTitle>

      <div class="feature-grid">
        <div v-for="(f, i) in features" :key="i" class="feature-item" :style="{ animationDelay: `${i * 0.1}s` }">
          <div class="feature-icon-box" :style="{ background: f.gradient }">
            <svg viewBox="0 0 24 24" fill="currentColor" class="feature-icon-svg">
              <path :d="f.path"/>
            </svg>
          </div>
          <div class="feature-text">
            <h3>{{ f.title }}</h3>
            <p>{{ f.description }}</p>
          </div>
          <div class="feature-number">{{ String(i + 1).padStart(2, '0') }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import SectionTitle from '@/components/common/SectionTitle.vue'

const features = [
  { title: '自然语言输入', description: '无需填写复杂表单，用日常语言描述你的旅行愿望，AI 自动理解并提取关键信息。', gradient: 'linear-gradient(135deg, #f59e0b, #d97706)', path: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z' },
  { title: 'AI 智能生成', description: '结合海量 POI 数据和实时信息，AI 生成包含景点、住宿、餐饮的完整行程方案。', gradient: 'linear-gradient(135deg, #8b5cf6, #7c3aed)', path: 'M13 10V3L4 14h7v7l9-11h-7z' },
  { title: '实时流式展示', description: '行程生成过程实时可见，像聊天一样自然，随时可以调整和优化。', gradient: 'linear-gradient(135deg, #3b82f6, #2563eb)', path: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' },
  { title: '灵活编辑调整', description: '支持拖拽调整、撤销重做，自由定制每一天的行程安排。', gradient: 'linear-gradient(135deg, #10b981, #059669)', path: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z' },
  { title: '动态重规划', description: '遇到航班延误、天气变化等情况，AI 自动生成备选方案，15分钟内确认。', gradient: 'linear-gradient(135deg, #ef4444, #dc2626)', path: 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15' },
  { title: '一键预订支付', description: '行程确定后，一键预订酒店、门票，支持延迟支付和订单管理。', gradient: 'linear-gradient(135deg, #f59e0b, #ea580c)', path: 'M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z' },
]
</script>

<style scoped lang="scss">
$bg-deep: #0a0e1a;
$bg-card: #111827;
$bg-elevated: #1a2235;
$text-primary: #f1f5f9;
$text-secondary: #94a3b8;
$text-muted: #64748b;
$border: #1e293b;

.feature-section { padding: var(--space-4xl) 0; background: $bg-deep; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 var(--space-lg); }

.feature-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: var(--space-2xl);
}

.feature-item {
  display: flex; align-items: flex-start; gap: 18px;
  padding: 28px;
  background: $bg-elevated;
  border-radius: 16px;
  border: 1px solid $border;
  position: relative; overflow: hidden;
  animation: fadeInUp 0.6s ease both;
  transition: all 0.3s ease;

  &::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(circle at 0% 0%, rgba(245,158,11,0.04), transparent 70%);
    opacity: 0; transition: opacity 0.3s;
  }

  &:hover {
    border-color: rgba(245, 158, 11, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    &::before { opacity: 1; }
  }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.feature-icon-box {
  width: 52px; height: 52px;
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  color: #fff;
}

.feature-icon-svg { width: 24px; height: 24px; }

.feature-text {
  flex: 1; min-width: 0;
  h3 { font-size: 16px; font-weight: 700; color: $text-primary; margin-bottom: 6px; }
  p { font-size: 13px; color: $text-muted; line-height: 1.65; }
}

.feature-number {
  font-size: 40px; font-weight: 800; color: rgba(255,255,255,0.03);
  position: absolute; top: 12px; right: 20px;
  font-family: 'SF Mono', 'Cascadia Code', 'Consolas', monospace;
  pointer-events: none;
}

@media (max-width: 768px) {
  .feature-grid { grid-template-columns: 1fr; }
  .feature-item { padding: 20px; }
}
</style>
