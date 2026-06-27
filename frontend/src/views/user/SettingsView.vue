<template>
  <div class="settings-view">
    <div class="view-header">
      <h3>偏好设置</h3>
      <p>设置你的旅行偏好，AI 将为你生成更精准的行程方案</p>
    </div>

    <div class="settings-cards">
      <div class="setting-card">
        <div class="card-icon style-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
        </div>
        <div class="card-content">
          <h4>旅行风格</h4>
          <p>选择你喜欢的旅行方式</p>
          <div class="checkbox-group">
            <label v-for="p in styleOptions" :key="p.value"
              class="pref-chip" :class="{ active: preferences.includes(p.value) }"
              @click="togglePref(p.value)">
              <span class="chip-emoji">{{ p.label.split(' ')[0] }}</span>
              <span class="chip-text">{{ p.label.split(' ')[1] }}</span>
            </label>
          </div>
        </div>
      </div>

      <div class="setting-card">
        <div class="card-icon budget-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        </div>
        <div class="card-content">
          <h4>预算范围</h4>
          <p>设置你的旅行预算区间</p>
          <div class="budget-slider">
            <div class="budget-control">
              <button class="budget-btn" @click="adjustBudget(-50)" :disabled="budget <= 500">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/></svg>
              </button>
              <div class="budget-value">
                <span class="budget-amount">¥{{ budget.toLocaleString() }}</span>
              </div>
              <button class="budget-btn" @click="adjustBudget(50)" :disabled="budget >= 20000">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
              </button>
            </div>
            <div class="budget-track">
              <input type="range" class="budget-range" :min="500" :max="20000" :step="50" v-model.number="budget" />
              <div class="budget-track-fill" :style="{ width: ((budget - 500) / (20000 - 500) * 100) + '%' }"></div>
            </div>
            <div class="budget-labels">
              <span class="budget-label">¥500</span>
              <span class="budget-label">¥20,000</span>
            </div>
          </div>
        </div>
      </div>

      <div class="setting-card">
        <div class="card-icon constraint-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        </div>
        <div class="card-content">
          <h4>旅行禁忌</h4>
          <p>告诉我们你不喜欢的事情</p>
          <div class="checkbox-group">
            <label v-for="c in constraintOptions" :key="c"
              class="constraint-chip" :class="{ active: constraints.includes(c) }"
              @click="toggleConstraint(c)">
              <svg v-if="constraints.includes(c)" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>
              <span>{{ c }}</span>
            </label>
          </div>
        </div>
      </div>
    </div>

    <div class="settings-actions">
      <button class="save-btn" :class="{ saving: saving }" @click="handleSave" :disabled="saving">
        <span class="save-btn-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
        </span>
        {{ saving ? '保存中...' : '保存设置' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { userAPI } from '@/api/user'

const preferences = ref<string[]>(['美食', '历史文化'])
const budget = ref(5000)
const constraints = ref<string[]>(['不爬山'])
const saving = ref(false)

const styleOptions = [
  { value: '美食', label: '🍜 美食' },
  { value: '历史文化', label: '🏛️ 历史文化' },
  { value: '自然风光', label: '🏔️ 自然风光' },
  { value: '购物', label: '🛍️ 购物' },
  { value: '亲子', label: '👨‍👩‍👧 亲子' },
  { value: '摄影', label: '📷 摄影' },
  { value: '探险', label: '🧗 探险' },
  { value: '休闲', label: '🌴 休闲' },
]

const constraintOptions = ['不爬山', '不早起', '不徒步', '不购物', '不吃辣']

function togglePref(val: string) {
  const idx = preferences.value.indexOf(val)
  if (idx >= 0) { preferences.value.splice(idx, 1) }
  else { preferences.value.push(val) }
}

function toggleConstraint(val: string) {
  const idx = constraints.value.indexOf(val)
  if (idx >= 0) { constraints.value.splice(idx, 1) }
  else { constraints.value.push(val) }
}

function adjustBudget(delta: number) {
  const newVal = budget.value + delta
  if (newVal >= 500 && newVal <= 20000) {
    budget.value = newVal
  }
}

async function handleSave() {
  saving.value = true
  try {
    await userAPI.updatePreferences({
      preferences: preferences.value,
      budget: budget.value,
      constraints: constraints.value,
    })
    ElMessage.success('设置已保存')
  } catch {
    ElMessage.error('保存失败，请重试')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped lang="scss">
.view-header {
  margin-bottom: var(--space-xl);

  h3 { font-size: var(--font-size-lg); font-weight: 700; margin: 0 0 var(--space-xs); }
  p { font-size: var(--font-size-sm); color: var(--color-text-secondary); margin: 0; }
}

.settings-cards {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.setting-card {
  display: flex;
  gap: var(--space-lg);
  padding: var(--space-xl);
  background: var(--color-bg);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  transition: border-color var(--transition-base), box-shadow var(--transition-base);

  &:hover {
    border-color: rgba(245, 158, 11, 0.25);
    box-shadow: 0 0 0 1px rgba(245, 158, 11, 0.05);
  }
}

// 卡片图标 — 内联 SVG 替代 el-icon
.card-icon {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: inset 0 -2px 0 rgba(0,0,0,0.12);

  svg {
    width: 24px;
    height: 24px;
    color: #fff;
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.15));
  }

  &.style-icon {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  }
  &.budget-icon {
    background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  }
  &.constraint-icon {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  }
}

.card-content {
  flex: 1;

  h4 { font-size: var(--font-size-base); font-weight: 600; color: var(--color-text-primary); margin: 0 0 4px; }
  p { font-size: var(--font-size-sm); color: var(--color-text-secondary); margin: 0 0 var(--space-md); }
}

// 自定义偏好标签 — 替代 el-checkbox-button
.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.pref-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 7px 14px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease;
  border: 1px solid var(--color-border);
  background: var(--color-bg-elevated);
  color: var(--color-text-secondary);

  .chip-emoji { font-size: 14px; line-height: 1; }
  .chip-text { font-weight: 500; }

  &:hover {
    border-color: rgba(245, 158, 11, 0.4);
    color: var(--color-text-primary);
    background: rgba(245, 158, 11, 0.06);
  }

  &.active {
    border-color: rgba(245, 158, 11, 0.4);
    background: rgba(245, 158, 11, 0.12);
    color: #f59e0b;

    .chip-text { font-weight: 600; }
  }
}

// 禁忌标签
.constraint-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease;
  border: 1px solid var(--color-border);
  background: var(--color-bg-elevated);
  color: var(--color-text-muted);

  svg { width: 13px; height: 13px; flex-shrink: 0; }

  &:hover {
    border-color: rgba(239, 68, 68, 0.3);
    color: var(--color-text-secondary);
  }

  &.active {
    border-color: rgba(239, 68, 68, 0.3);
    background: rgba(239, 68, 68, 0.08);
    color: #f87171;

    svg { stroke: #f87171; }
  }
}

// 预算滑块 — 完全自定义，替代 el-slider + show-input
.budget-slider {
  max-width: 420px;
}

.budget-control {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.budget-btn {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  background: var(--color-bg-elevated);
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.2s ease;
  flex-shrink: 0;

  svg { width: 16px; height: 16px; }

  &:hover:not(:disabled) {
    border-color: rgba(139, 92, 246, 0.4);
    color: #8b5cf6;
    background: rgba(139, 92, 246, 0.08);
  }

  &:active:not(:disabled) {
    transform: scale(0.95);
  }

  &:disabled {
    opacity: 0.35;
    cursor: not-allowed;
  }
}

.budget-value {
  flex: 1;
  text-align: center;
  padding: 8px 0;
}

.budget-amount {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -0.5px;
}

.budget-track {
  position: relative;
  height: 6px;
  background: var(--color-border);
  border-radius: 3px;
  cursor: pointer;
}

.budget-range {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px;
  background: transparent;
  outline: none;
  position: relative;
  z-index: 2;
  cursor: pointer;

  &::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #fff;
    border: 3px solid #8b5cf6;
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15), 0 2px 8px rgba(0,0,0,0.2);
    cursor: pointer;
    transition: box-shadow 0.2s ease;

    &:hover {
      box-shadow: 0 0 0 6px rgba(139, 92, 246, 0.2), 0 2px 12px rgba(0,0,0,0.25);
    }
  }

  &::-moz-range-thumb {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #fff;
    border: 3px solid #8b5cf6;
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15), 0 2px 8px rgba(0,0,0,0.2);
    cursor: pointer;
  }
}

.budget-track-fill {
  position: absolute;
  top: 0;
  left: 0;
  height: 6px;
  background: linear-gradient(90deg, #8b5cf6, #a78bfa);
  border-radius: 3px 0 0 3px;
  pointer-events: none;
  z-index: 1;
}

.budget-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 6px;
}
.budget-label {
  font-size: 11px;
  color: var(--color-text-muted);
  font-weight: 500;
}

// 保存按钮 — 替代 el-button
.settings-actions {
  margin-top: var(--space-xl);
  display: flex;
  justify-content: flex-end;
}

.save-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 32px;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: #1a1a1a;
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.25s ease;
  box-shadow: 0 2px 16px rgba(245, 158, 11, 0.3);

  .save-btn-icon {
    display: flex;
    svg { width: 18px; height: 18px; }
  }

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 22px rgba(245, 158, 11, 0.45);
    filter: brightness(1.08);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.65;
    cursor: not-allowed;
  }

  &.saving {
    animation: pulse 1.5s ease infinite;
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.75; }
}
</style>
