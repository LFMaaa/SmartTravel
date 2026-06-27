<template>
  <div class="payment-panel">
    <h4>支付信息</h4>

    <!-- Resource lock countdown -->
    <div class="lock-section" :class="{ expired: remaining <= 0 }">
      <div class="lock-header">
        <el-icon><Clock /></el-icon>
        <span>资源锁定倒计时</span>
      </div>
      <div class="lock-countdown">{{ formatCountdown }}</div>
      <div class="lock-hint" v-if="remaining > 0">请在倒计时结束前完成支付，否则资源将被释放</div>
      <div class="lock-hint expired-hint" v-else>资源已释放，请重新预订</div>
    </div>

    <!-- Cost breakdown -->
    <div class="cost-section">
      <div class="cost-row" v-for="item in items" :key="item.label">
        <span class="cost-label">{{ item.label }}</span>
        <span class="cost-amount">¥{{ item.amount.toLocaleString() }}</span>
      </div>
      <div class="cost-row discount" v-if="discount">
        <span class="cost-label">会员折扣</span>
        <span class="cost-amount discount-amount">-¥{{ discount.toLocaleString() }}</span>
      </div>
      <div class="cost-divider" />
      <div class="cost-row total">
        <span class="cost-label">合计</span>
        <span class="cost-amount total-amount">¥{{ totalAmount.toLocaleString() }}</span>
      </div>
    </div>

    <!-- Payment method -->
    <div class="method-section">
      <h5>支付方式</h5>
      <div class="method-options">
        <button
          :class="['method-option', { active: method === 'wechat' }]"
          @click="method = 'wechat'"
        >
          <span class="method-icon">💚</span>
          <span>微信支付</span>
        </button>
        <button
          :class="['method-option', { active: method === 'alipay' }]"
          @click="method = 'alipay'"
        >
          <span class="method-icon">💙</span>
          <span>支付宝</span>
        </button>
      </div>
    </div>

    <!-- Pay button -->
    <el-button
      type="primary"
      size="large"
      class="pay-btn"
      :disabled="remaining <= 0 || totalAmount <= 0"
      :loading="paying"
      @click="$emit('pay', method)"
    >
      {{ remaining <= 0 ? '已过期' : `确认支付 ¥${totalAmount.toLocaleString()}` }}
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Clock } from '@element-plus/icons-vue'

interface CostItem {
  label: string
  amount: number
}

const props = defineProps<{
  items: CostItem[]
  discount?: number
  remaining: number
  paying?: boolean
}>()

defineEmits<{ pay: [method: string] }>()

const method = ref('wechat')

const totalAmount = computed(() => {
  const sum = props.items.reduce((s, i) => s + i.amount, 0)
  return Math.max(0, sum - (props.discount || 0))
})

const formatCountdown = computed(() => {
  if (props.remaining <= 0) return '00:00'
  const m = Math.floor(props.remaining / 60)
  const s = props.remaining % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
})
</script>

<style scoped lang="scss">
.payment-panel {
  padding: var(--space-xl);
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);

  h4 { font-size: var(--font-size-lg); font-weight: 700; margin-bottom: var(--space-lg); color: var(--color-text-primary); }
  h5 { font-size: var(--font-size-sm); font-weight: 600; margin-bottom: var(--space-sm); color: var(--color-text-primary); }
}

.lock-section {
  padding: var(--space-md) var(--space-lg);
  background: var(--color-warning-light);
  border-radius: var(--radius-md);
  text-align: center;
  margin-bottom: var(--space-xl);

  &.expired {
    background: var(--color-danger-light);
    .lock-countdown { color: var(--color-danger); }
  }
}

.lock-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-sm);
}

.lock-countdown {
  font-size: var(--font-size-2xl);
  font-weight: 800;
  color: var(--color-warning);
  font-family: monospace;
}

.lock-hint {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  margin-top: 4px;
}

.expired-hint { color: var(--color-danger); font-weight: 600; }

.cost-section {
  margin-bottom: var(--space-xl);
}

.cost-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  font-size: var(--font-size-sm);
}

.cost-label { color: var(--color-text-secondary); }
.cost-amount { font-weight: 600; color: var(--color-text-primary); }

.discount-amount { color: var(--color-success); }

.cost-divider {
  height: 1px;
  background: var(--color-border-light);
  margin: var(--space-sm) 0;
}

.total {
  .cost-label { font-size: var(--font-size-base); font-weight: 600; color: var(--color-text-primary); }
  .total-amount { font-size: var(--font-size-xl); font-weight: 800; color: var(--color-primary); }
}

.method-section {
  margin-bottom: var(--space-xl);
}

.method-options {
  display: flex;
  gap: var(--space-md);
}

.method-option {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  padding: var(--space-md);
  background: var(--color-bg);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: 500;
  cursor: pointer;
  font-family: var(--font-family);
  transition: all var(--transition-base);

  &:hover { border-color: var(--color-primary); }
  &.active {
    border-color: var(--color-primary);
    background: var(--color-primary-lighter);
  }
}

.method-icon { font-size: 20px; }

.pay-btn {
  width: 100%;
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-weight: 600;
  padding: 14px 0;
}
</style>
