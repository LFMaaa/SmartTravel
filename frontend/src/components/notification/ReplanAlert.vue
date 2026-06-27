<template>
  <el-dialog
    v-model="visible"
    title="行程变动提醒"
    width="600px"
    :close-on-click-modal="false"
  >
    <el-alert
      :title="displayTitle"
      type="warning"
      :description="displayDesc"
      show-icon
      :closable="false"
    />
    <div class="alternatives" style="margin-top: 20px">
      <h4>AI 为您生成了 {{ alternatives.length }} 套备选方案：</h4>
      <el-radio-group v-model="selectedPlan">
        <el-card
          v-for="plan in alternatives"
          :key="plan.plan_id"
          class="plan-card"
          :class="{ selected: selectedPlan === plan.plan_id }"
          shadow="hover"
        >
          <el-radio :value="plan.plan_id">
            <strong>{{ plan.title }}</strong>
          </el-radio>
          <p class="plan-desc">{{ plan.description }}</p>
          <p class="plan-impact">{{ plan.impact }}</p>
        </el-card>
      </el-radio-group>
    </div>
    <div class="countdown-section">
      <span>方案将在 </span>
      <CountdownTimer :remaining="countdown" />
      <span> 后过期</span>
    </div>
    <template #footer>
      <el-button @click="handleIgnore">忽略</el-button>
      <el-button type="primary" @click="handleConfirm" :disabled="!selectedPlan">
        确认选择
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import CountdownTimer from '@/components/payment/CountdownTimer.vue'

interface Alternative {
  plan_id: string
  title: string
  description: string
  impact: string
}

const props = defineProps<{
  visible: boolean
  alternatives: Alternative[]
  countdown: number
  alertTitle?: string
  alertDesc?: string
}>()

const emit = defineEmits<{
  'update:visible': [boolean]
  confirm: [planId: string]
  ignore: []
}>()

const selectedPlan = ref('')

const displayTitle = computed(() => props.alertTitle || '行程变动提醒')
const displayDesc = computed(() => props.alertDesc || '您的行程受到了影响，AI 已为您生成备选方案。')

function handleConfirm() {
  if (selectedPlan.value) {
    emit('confirm', selectedPlan.value)
  }
}

function handleIgnore() {
  emit('update:visible', false)
  emit('ignore')
}
</script>

<style scoped>
.plan-card { margin-bottom: 12px; cursor: pointer; }
.plan-card.selected { border-color: #409eff; }
.plan-desc { margin: 8px 0 0 24px; font-size: 13px; color: #606266; }
.plan-impact { margin: 4px 0 0 24px; font-size: 12px; color: #909399; }
.countdown-section {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  font-size: 14px;
  color: #606266;
}
</style>