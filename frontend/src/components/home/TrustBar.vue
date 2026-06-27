<template>
  <section class="trust-section">
    <div class="trust-bg">
      <div class="trust-orb orb-a"></div>
      <div class="trust-orb orb-b"></div>
    </div>
    <div class="container">
      <div class="trust-content">
        <h3 class="trust-headline">
          已有 <span class="text-gradient">10,000+</span> 旅行者<br />通过智游规划完美旅程
        </h3>
        <div class="trust-grid">
          <div v-for="item in stats" :key="item.label" class="trust-item">
            <svg viewBox="0 0 24 24" fill="currentColor" class="trust-icon">
              <path :d="item.path"/>
            </svg>
            <span class="trust-value">{{ item.value }}</span>
            <span class="trust-label">{{ item.label }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const stats = [
  { value: '4.9', label: '用户评分', path: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z' },
  { value: '500+', label: '合作供应商', path: 'M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1' },
  { value: '银行级', label: '数据加密', path: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z' },
  { value: '7×24', label: '智能客服', path: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z' },
]
</script>

<style scoped lang="scss">
$bg-deep: #0a0e1a;
$bg-card: #111827;
$brand-amber: #f59e0b;
$text-primary: #f1f5f9;
$text-muted: #64748b;
$border: #1e293b;

.trust-section {
  padding: var(--space-3xl) 0;
  background: $bg-card;
  position: relative; overflow: hidden;
}

.trust-bg { position: absolute; inset: 0; }
.trust-orb {
  position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.06;
  &.orb-a { width: 400px; height: 400px; background: #f59e0b; top: -100px; right: -100px; }
  &.orb-b { width: 350px; height: 350px; background: #3b82f6; bottom: -100px; left: -100px; }
}

.container { max-width: 1200px; margin: 0 auto; padding: 0 var(--space-lg); position: relative; z-index: 1; }
.trust-content { text-align: center; }

.trust-headline {
  font-size: 32px; font-weight: 700; color: $text-primary;
  line-height: 1.4; margin-bottom: var(--space-2xl);
}

.text-gradient {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}

.trust-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;
}

.trust-item {
  display: flex; flex-direction: column; align-items: center;
  gap: 10px; padding: var(--space-xl);
  background: rgba(255,255,255,0.03);
  border-radius: 16px;
  border: 1px solid $border;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-4px);
    border-color: rgba(245, 158, 11, 0.2);
    background: rgba(245, 158, 11, 0.04);
  }
}

.trust-icon { width: 28px; height: 28px; color: $brand-amber; }

.trust-value {
  font-size: 30px; font-weight: 800; color: $text-primary;
}

.trust-label { font-size: 13px; color: $text-muted; }

@media (max-width: 768px) {
  .trust-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .trust-headline { font-size: 24px; }
}
</style>
