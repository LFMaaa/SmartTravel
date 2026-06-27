<template>
  <section class="hero-section">
    <!-- Background orbs -->
    <div class="hero-bg">
      <div class="bg-orb orb-1"></div>
      <div class="bg-orb orb-2"></div>
      <div class="bg-orb orb-3"></div>
      <div class="bg-grid"></div>
    </div>

    <div class="hero-content">
      <div class="hero-badge">
        <span class="badge-dot"></span>
        <span>AI 驱动 · 智能旅行规划</span>
      </div>

      <h1 class="hero-headline">
        <span class="line-1">说出你的旅行愿望</span>
        <span class="line-2">
          AI 为你定制 <span class="text-gradient">完美行程</span>
        </span>
      </h1>

      <p class="hero-desc">
        只需一句话描述你的旅行梦想，AI 智能规划每一天的景点、住宿、餐饮和交通
      </p>

      <!-- Search input -->
      <div class="hero-search">
        <div class="search-wrapper">
          <span class="search-prefix">
            <svg viewBox="0 0 20 20" fill="currentColor"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/></svg>
          </span>
          <input
            v-model="query"
            class="search-input"
            placeholder="描述你的旅行需求，例如：带父母去北京5天，预算1.5万..."
            @keyup.enter="startGenerate"
          />
          <button v-if="query" class="clear-btn" @click="query = ''">
            <svg viewBox="0 0 16 16" fill="currentColor"><path d="M4.293 4.293a1 1 0 011.414 0L8 6.586l2.293-2.293a1 1 0 011.414 1.414L9.414 8l2.293 2.293a1 1 0 01-1.414 1.414L8 9.414l-2.293 2.293a1 1 0 01-1.414-1.414L6.586 8 4.293 5.707a1 1 0 010-1.414z"/></svg>
          </button>
          <button class="generate-btn" :disabled="loading" @click="startGenerate">
            <span v-if="!loading">
              <svg viewBox="0 0 20 20" fill="currentColor" class="btn-icon"><path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/></svg>
              开始规划
            </span>
            <span v-else class="btn-loading">
              <svg class="spinner" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="31.4 31.4" stroke-linecap="round"/></svg>
              生成中...
            </span>
          </button>
        </div>
      </div>

      <!-- Quick suggestions -->
      <div class="quick-suggestions">
        <span class="suggest-label">试试这些：</span>
        <button v-for="s in suggestions" :key="s" class="suggest-chip" @click="quickStart(s)">{{ s }}</button>
      </div>

      <!-- Stats -->
      <div class="hero-stats">
        <div class="stat-item">
          <span class="stat-value">10,000+</span>
          <span class="stat-label">已生成行程</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-value">500+</span>
          <span class="stat-label">热门目的地</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-value">98%</span>
          <span class="stat-label">用户满意度</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const query = ref('')
const loading = ref(false)

const suggestions = ['带爸妈去北京4天', '和朋友去成都吃美食', '一个人去云南发呆']

function startGenerate() {
  if (!query.value.trim()) return
  loading.value = true
  router.push({ name: 'itinerary-generate', query: { q: query.value } })
}

function quickStart(text: string) {
  query.value = text
  startGenerate()
}
</script>

<style scoped lang="scss">
$bg-deep: #0a0e1a;
$bg-card: #111827;
$bg-elevated: #1a2235;
$brand-amber: #f59e0b;
$brand-amber-light: #fbbf24;
$brand-blue: #3b82f6;
$text-primary: #f1f5f9;
$text-secondary: #94a3b8;
$text-muted: #64748b;
$border: #1e293b;

.hero-section {
  position: relative;
  min-height: 92vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: var(--space-4xl) var(--space-lg);
  background: $bg-deep;
}

.hero-bg {
  position: absolute; inset: 0;
  overflow: hidden;
}

.bg-orb {
  position: absolute; border-radius: 50%; filter: blur(120px); opacity: 0.06;
  &.orb-1 { width: 600px; height: 600px; background: #f59e0b; top: -200px; right: -100px; animation: orb-drift 25s ease-in-out infinite; }
  &.orb-2 { width: 500px; height: 500px; background: #3b82f6; bottom: -150px; left: -150px; animation: orb-drift 30s ease-in-out infinite reverse; }
  &.orb-3 { width: 400px; height: 400px; background: #8b5cf6; top: 40%; left: 50%; animation: orb-drift 20s ease-in-out infinite; }
}

@keyframes orb-drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(40px, -30px) scale(1.08); }
  66% { transform: translate(-30px, 25px) scale(0.94); }
}

.bg-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
  background-size: 60px 60px;
}

.hero-content {
  position: relative; z-index: 2;
  text-align: center;
  max-width: 760px;
}

.hero-badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 20px;
  background: rgba(245, 158, 11, 0.08);
  border: 1px solid rgba(245, 158, 11, 0.15);
  border-radius: var(--radius-full);
  font-size: 13px; font-weight: 600;
  color: $brand-amber;
  margin-bottom: var(--space-xl);
}

.badge-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: $brand-amber;
  animation: pulse-glow 2s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 4px $brand-amber; }
  50% { box-shadow: 0 0 12px $brand-amber, 0 0 24px rgba(245,158,11,0.3); }
}

.hero-headline {
  margin-bottom: var(--space-lg);
  .line-1 { display: block; font-size: 28px; font-weight: 600; color: $text-secondary; margin-bottom: var(--space-sm); }
  .line-2 { display: block; font-size: 54px; font-weight: 800; color: $text-primary; line-height: 1.12; }
}

.text-gradient {
  background: linear-gradient(135deg, $brand-amber-light, $brand-amber);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 17px; color: $text-muted;
  margin-bottom: var(--space-2xl);
  max-width: 520px; margin-left: auto; margin-right: auto;
  line-height: 1.7;
}

.hero-search { margin-bottom: var(--space-xl); }

.search-wrapper {
  display: flex; align-items: center;
  background: $bg-elevated;
  border: 1.5px solid $border;
  border-radius: 14px;
  padding: 5px 5px 5px 16px;
  transition: all 0.3s ease;
  height: 64px;

  &:focus-within {
    border-color: $brand-amber;
    box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.08);
  }
}

.search-prefix {
  color: $text-muted; flex-shrink: 0;
  svg { width: 20px; height: 20px; }
}

.search-input {
  flex: 1; border: none; outline: none;
  font-size: 15px; font-family: inherit;
  color: $text-primary; padding: 0 14px;
  background: transparent;
  &::placeholder { color: $text-muted; font-size: 14px; }
}

.clear-btn {
  flex-shrink: 0; width: 28px; height: 28px;
  border: none; background: none; color: $text-muted;
  cursor: pointer; border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
  svg { width: 16px; height: 16px; }
  &:hover { color: $text-primary; background: rgba(255,255,255,0.05); }
}

.generate-btn {
  flex-shrink: 0; height: 52px; min-width: 130px;
  border: none; border-radius: 12px;
  font-size: 15px; font-weight: 600;
  cursor: pointer;
  color: #0f172a;
  background: linear-gradient(135deg, $brand-amber-light, $brand-amber);
  box-shadow: 0 4px 16px rgba(245, 158, 11, 0.25);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: inherit;
  display: flex; align-items: center; gap: 6px;
  padding: 0 24px;

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 6px 24px rgba(245, 158, 11, 0.35);
  }
  &:disabled { opacity: 0.6; cursor: not-allowed; }
}

.btn-icon { width: 18px; height: 18px; }

.spinner {
  width: 20px; height: 20px;
  animation: spin 0.8s linear infinite;
  circle { stroke-dashoffset: 0; }
}

@keyframes spin { to { transform: rotate(360deg); } }

.btn-loading {
  display: inline-flex; align-items: center; gap: 8px;
}

.quick-suggestions {
  display: flex; align-items: center; justify-content: center;
  gap: 8px; flex-wrap: wrap; margin-bottom: var(--space-3xl);
}

.suggest-label { font-size: 12px; color: $text-muted; margin-right: 4px; }

.suggest-chip {
  padding: 7px 18px;
  background: $bg-elevated;
  border: 1px solid $border;
  border-radius: var(--radius-full);
  font-size: 13px; color: $text-muted;
  cursor: pointer; font-family: inherit;
  transition: all 0.25s ease;

  &:hover {
    border-color: $brand-amber;
    color: $brand-amber;
    background: rgba(245, 158, 11, 0.06);
  }
}

.hero-stats {
  display: flex; align-items: center; justify-content: center;
  gap: var(--space-xl);
  padding: var(--space-lg) var(--space-xl);
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--radius-lg);
  border: 1px solid $border;
}

.stat-item { text-align: center; }
.stat-value { display: block; font-size: 26px; font-weight: 800; color: $brand-amber; }
.stat-label { display: block; font-size: 11px; color: $text-muted; margin-top: 2px; }
.stat-divider { width: 1px; height: 36px; background: $border; }

@media (max-width: 768px) {
  .hero-headline {
    .line-1 { font-size: 20px; }
    .line-2 { font-size: 30px; }
  }
  .search-wrapper { flex-wrap: wrap; height: auto; padding: 8px; gap: 8px;
    .search-prefix { display: none; }
    .generate-btn { width: 100%; }
  }
  .hero-stats { flex-wrap: wrap; gap: var(--space-md); }
}
</style>
