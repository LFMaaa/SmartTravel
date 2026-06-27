<template>
  <Teleport to="body">
    <transition name="replan-slide">
      <div v-if="visible" class="replan-overlay" @click.self="handleIgnore">
        <div class="replan-panel">
          <!-- Header -->
          <div class="replan-header">
            <div class="header-icon">
              <el-icon :size="24"><WarningFilled /></el-icon>
            </div>
            <div class="header-text">
              <h3>{{ alertTitle || '行程变动提醒' }}</h3>
              <p>{{ alertDesc || '你的行程受到了影响，AI 已为你生成新行程方案' }}</p>
            </div>
            <el-button text class="header-close" @click="handleIgnore">
              <el-icon :size="18"><Close /></el-icon>
            </el-button>
          </div>

          <!-- Plan Tabs -->
          <div class="plan-tabs">
            <button
              v-for="(plan, idx) in plans"
              :key="plan.plan_id"
              :class="['plan-tab', { active: activePlan === idx }]"
              @click="activePlan = idx"
            >
              <span class="tab-label">{{ plan.title }}</span>
              <el-tag v-if="idx === 0" size="small" type="success" effect="dark" round>推荐</el-tag>
            </button>
          </div>

          <!-- Plan Content -->
          <div class="plan-content">
            <transition name="fade" mode="out-in">
              <div :key="activePlan" class="plan-detail">
                <div class="plan-reason" v-if="currentPlan.reason">
                  <el-icon><InfoFilled /></el-icon>
                  <span>{{ currentPlan.reason }}</span>
                </div>

                <!-- Comparison -->
                <div class="comparison">
                  <div class="compare-section">
                    <h5 class="compare-label old">原行程</h5>
                    <div class="compare-items">
                      <div
                        v-for="item in currentPlan.oldItems"
                        :key="item"
                        class="compare-item old-item"
                      >
                        <s>{{ item }}</s>
                      </div>
                    </div>
                  </div>
                  <div class="compare-arrow">
                    <el-icon :size="20"><Right /></el-icon>
                  </div>
                  <div class="compare-section">
                    <h5 class="compare-label new">新行程</h5>
                    <div class="compare-items">
                      <div
                        v-for="item in currentPlan.newItems"
                        :key="item.name"
                        class="compare-item new-item"
                      >
                        <el-tag size="small" type="primary" round class="new-badge">新</el-tag>
                        <span>{{ item.name }}</span>
                        <span class="item-cost" v-if="item.costDiff">
                          {{ item.costDiff > 0 ? `+¥${item.costDiff}` : `-¥${Math.abs(item.costDiff)}` }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Impact -->
                <div class="plan-impact">
                  <div class="impact-item">
                    <span class="impact-label">体验影响</span>
                    <span class="impact-value" :class="currentPlan.impactLevel">
                      {{ currentPlan.impact }}
                    </span>
                  </div>
                  <div class="impact-item">
                    <span class="impact-label">成本变化</span>
                    <span class="impact-value" :class="currentPlan.costChange >= 0 ? 'up' : 'down'">
                      {{ currentPlan.costChange >= 0 ? `+¥${currentPlan.costChange}` : `-¥${Math.abs(currentPlan.costChange)}` }}
                    </span>
                  </div>
                </div>
              </div>
            </transition>
          </div>

          <!-- Footer -->
          <div class="replan-footer">
            <div class="countdown-section" :class="{ urgent: countdown <= 300 }">
              <el-icon><Clock /></el-icon>
              <span class="countdown-text">{{ formatCountdown }}</span>
              <span class="countdown-hint">后方案过期</span>
            </div>
            <div class="footer-actions">
              <el-button size="large" @click="handleIgnore">手动调整</el-button>
              <el-button size="large" type="primary" :disabled="!currentPlan" @click="handleConfirm">
                确认选择
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch, onUnmounted } from 'vue'
import { WarningFilled, Close, InfoFilled, Right, Clock } from '@element-plus/icons-vue'

interface PlanItem {
  name: string
  costDiff?: number
}

interface Plan {
  plan_id: string
  title: string
  description: string
  reason?: string
  impact: string
  impactLevel: 'low' | 'medium' | 'high'
  costChange: number
  oldItems: string[]
  newItems: PlanItem[]
}

const props = defineProps<{
  visible: boolean
  plans: Plan[]
  countdown: number
  alertTitle?: string
  alertDesc?: string
}>()

const emit = defineEmits<{
  'update:visible': [boolean]
  confirm: [planId: string]
  ignore: []
}>()

const activePlan = ref(0)
let timer: ReturnType<typeof setInterval> | null = null
const remaining = ref(props.countdown)

const currentPlan = computed(() => props.plans[activePlan.value] || props.plans[0])

const formatCountdown = computed(() => {
  const m = Math.floor(remaining.value / 60)
  const s = remaining.value % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
})

watch(() => props.visible, (val) => {
  if (val) {
    remaining.value = props.countdown
    timer = setInterval(() => {
      remaining.value = Math.max(0, remaining.value - 1)
      // Browser notification at 5 min mark
      if (remaining.value === 300 && 'Notification' in window && Notification.permission === 'granted') {
        new Notification('智游提醒', { body: '行程方案将在5分钟后过期，请尽快确认' })
      }
    }, 1000)
  } else {
    if (timer) { clearInterval(timer); timer = null }
  }
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

function handleConfirm() {
  if (currentPlan.value) {
    emit('confirm', currentPlan.value.plan_id)
  }
}

function handleIgnore() {
  emit('update:visible', false)
  emit('ignore')
}
</script>

<style scoped lang="scss">
.replan-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 3000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.replan-panel {
  width: 680px;
  max-height: 90vh;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

// Header
.replan-header {
  display: flex;
  align-items: flex-start;
  gap: var(--space-md);
  padding: var(--space-xl);
  background: var(--gradient-primary);
  color: #fff;
}

.header-icon {
  flex-shrink: 0;
  animation: pulse-glow 2s ease-in-out infinite;
}

.header-text {
  flex: 1;
  h3 { font-size: var(--font-size-lg); font-weight: 700; margin-bottom: 4px; }
  p { font-size: var(--font-size-sm); opacity: 0.9; line-height: 1.5; }
}

.header-close {
  color: rgba(255, 255, 255, 0.7);
  &:hover { color: #fff; }
}

// Tabs
.plan-tabs {
  display: flex;
  border-bottom: 1px solid var(--color-border-light);
}

.plan-tab {
  flex: 1;
  padding: var(--space-md);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  font-family: var(--font-family);
  transition: all var(--transition-base);

  &:hover { color: var(--color-primary); }
  &.active {
    color: var(--color-primary);
    border-bottom-color: var(--color-primary);
    font-weight: 600;
  }
}

.tab-label { }

// Content
.plan-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-lg);
}

.plan-reason {
  display: flex;
  align-items: flex-start;
  gap: var(--space-sm);
  padding: var(--space-md);
  background: var(--color-info-light);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  color: var(--color-primary-dark);
  margin-bottom: var(--space-lg);
}

.comparison {
  display: flex;
  gap: var(--space-md);
  align-items: flex-start;
  margin-bottom: var(--space-lg);
}

.compare-section {
  flex: 1;
}

.compare-label {
  font-size: var(--font-size-xs);
  font-weight: 600;
  margin-bottom: var(--space-sm);
  &.old { color: var(--color-text-muted); }
  &.new { color: var(--color-primary); }
}

.compare-items {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.compare-item {
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-sm);

  &.old-item {
    background: var(--color-bg);
    color: var(--color-text-muted);
  }

  &.new-item {
    background: var(--color-primary-lighter);
    color: var(--color-text-primary);
    display: flex;
    align-items: center;
    gap: var(--space-sm);
  }
}

.new-badge {
  flex-shrink: 0;
}

.item-cost {
  margin-left: auto;
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--color-warning);
}

.compare-arrow {
  display: flex;
  align-items: center;
  padding-top: 24px;
  color: var(--color-primary);
}

// Impact
.plan-impact {
  display: flex;
  gap: var(--space-lg);
}

.impact-item {
  flex: 1;
  padding: var(--space-md);
  background: var(--color-bg);
  border-radius: var(--radius-md);
}

.impact-label {
  display: block;
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  margin-bottom: 4px;
}

.impact-value {
  font-size: var(--font-size-base);
  font-weight: 700;

  &.low { color: var(--color-success); }
  &.medium { color: var(--color-warning); }
  &.high { color: var(--color-danger); }
  &.up { color: var(--color-danger); }
  &.down { color: var(--color-success); }
}

// Footer
.replan-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-lg) var(--space-xl);
  border-top: 1px solid var(--color-border-light);
  background: var(--color-bg);
}

.countdown-section {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);

  &.urgent {
    color: var(--color-danger);
    animation: pulse-scale 1s ease-in-out infinite;
  }
}

.countdown-text {
  font-size: var(--font-size-xl);
  font-weight: 800;
  font-family: monospace;
}

.footer-actions {
  display: flex;
  gap: var(--space-sm);
}

// Slide transition
.replan-slide-enter-active { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
.replan-slide-leave-active { transition: all 0.3s ease; }
.replan-slide-enter-from {
  opacity: 0;
  .replan-panel { transform: translateX(60px); }
}
.replan-slide-leave-to {
  opacity: 0;
  .replan-panel { transform: translateX(60px); }
}

@media (max-width: 768px) {
  .replan-panel { width: 95vw; max-height: 95vh; }
  .comparison { flex-direction: column; }
  .compare-arrow { transform: rotate(90deg); padding: 0; }
  .replan-footer { flex-direction: column; gap: var(--space-md); }
}
</style>
