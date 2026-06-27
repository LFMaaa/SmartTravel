<template>
  <div class="payment-view">
    <div class="payment-container">
      <!-- Left: Booking List -->
      <div class="booking-section">
        <div class="section-header">
          <el-button text @click="$router.back()">
            <el-icon><ArrowLeft /></el-icon>
            返回
          </el-button>
          <h3>预订清单</h3>
        </div>

        <!-- Grouped by resource type -->
        <div v-for="group in bookingGroups" :key="group.type" class="booking-group">
          <div class="group-header" @click="toggleGroup(group.type)">
            <el-icon :size="16">
              <CaretRight v-if="!expandedGroups.includes(group.type)" />
              <CaretBottom v-else />
            </el-icon>
            <span class="group-label">{{ group.label }}</span>
            <span class="group-count">{{ group.items.length }}项</span>
            <span class="group-total">¥{{ group.total.toLocaleString() }}</span>
          </div>
          <div v-show="expandedGroups.includes(group.type)" class="group-items">
            <BookingItem
              v-for="item in group.items"
              :key="item.id"
              :name="item.name"
              :resource-type="item.resourceType"
              :price="item.price"
              :status="item.status"
              :date="item.date"
              :time="(item as any).time"
              @find-alternative="handleFindAlternative(item)"
            />
          </div>
        </div>

        <el-empty v-if="bookingGroups.length === 0" description="暂无预订项目" />
      </div>

      <!-- Right: Payment Panel -->
      <div class="payment-section">
        <ResourceLock
          :remaining="remaining"
          :total-duration="900"
        />

        <PaymentPanel
          :items="costItems"
          :discount="memberDiscount"
          :remaining="remaining"
          :paying="paying"
          @pay="handlePay"
        />
      </div>
    </div>

    <!-- Payment success dialog -->
    <el-dialog
      v-model="successVisible"
      title="支付成功"
      width="400px"
      center
      :close-on-click-modal="false"
    >
      <div class="success-content">
        <el-icon :size="56" class="success-icon"><CircleCheckFilled /></el-icon>
        <h3>预订完成！</h3>
        <p>你的行程相关资源已预订成功</p>
        <div class="success-actions">
          <el-button type="primary" @click="$router.push('/user/itineraries')">
            返回我的行程
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { paymentAPI } from '@/api/payment'
import BookingItem from '@/components/payment/BookingItem.vue'
import PaymentPanel from '@/components/payment/PaymentPanel.vue'
import ResourceLock from '@/components/payment/ResourceLock.vue'
import {
  ArrowLeft, CaretRight, CaretBottom, CircleCheckFilled,
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const paying = ref(false)
const successVisible = ref(false)

// Countdown: 15 minutes
const remaining = ref(900)
let timer: ReturnType<typeof setInterval> | null = null

const expandedGroups = ref<string[]>(['hotel', 'ticket', 'restaurant'])

// Mock booking data
const bookingGroups = computed(() => [
  {
    type: 'hotel',
    label: '🏨 酒店',
    items: [
      { id: '1', name: '北京王府井希尔顿酒店', resourceType: 'hotel' as const, price: 1280, status: 'locked' as const, date: '2026-07-01', time: '14:00' },
      { id: '2', name: '成都春熙路亚朵酒店', resourceType: 'hotel' as const, price: 680, status: 'locked' as const, date: '2026-07-04', time: '14:00' },
    ],
    total: 1960,
  },
  {
    type: 'ticket',
    label: '🎫 门票',
    items: [
      { id: '3', name: '故宫博物院', resourceType: 'ticket' as const, price: 60, status: 'locked' as const, date: '2026-07-01' },
      { id: '4', name: '八达岭长城', resourceType: 'ticket' as const, price: 40, status: 'pending' as const, date: '2026-07-02' },
    ],
    total: 100,
  },
  {
    type: 'restaurant',
    label: '🍜 餐饮',
    items: [
      { id: '5', name: '全聚德烤鸭店（前门店）', resourceType: 'restaurant' as const, price: 300, status: 'locked' as const, date: '2026-07-01', time: '18:00' },
    ],
    total: 300,
  },
])

const costItems = computed(() => [
  { label: '酒店', amount: 1960 },
  { label: '门票', amount: 100 },
  { label: '餐饮', amount: 300 },
  { label: '服务费', amount: 50 },
])

const memberDiscount = ref(100) // Mock member discount

const totalAmount = computed(() => {
  const sum = costItems.value.reduce((s, i) => s + i.amount, 0)
  return Math.max(0, sum - memberDiscount.value)
})

function toggleGroup(type: string) {
  const idx = expandedGroups.value.indexOf(type)
  if (idx >= 0) expandedGroups.value.splice(idx, 1)
  else expandedGroups.value.push(type)
}

async function handlePay(method: string) {
  if (paying.value) return
  if (!userStore.user?.id) {
    router.push('/login?redirect=/itinerary/payment')
    return
  }

  paying.value = true
  try {
    // 收集所有预订项
    const items = bookingGroups.value.flatMap(g => g.items.map(item => ({
      resource_type: item.resourceType,
      resource_name: item.name,
      unit_price: item.price,
      quantity: 1,
    })))

    // 调用后端创建预订支付订单
    const { data } = await paymentAPI.createBookingOrder({
      user_id: userStore.user.id,
      total_amount: totalAmount.value,
      items,
      return_url: `${window.location.origin}/itinerary/payment?paid=1`,
    })

    const result = data.data

    if (result.alipay_url) {
      // 跳转到支付宝沙箱支付页面
      window.location.href = result.alipay_url
      // 页面即将离开，倒计时会在 unloaded 时自动清理
      return
    } else {
      // 沙箱模式：模拟支付
      ElMessage.info('沙箱模式：正在模拟支付...')
      await new Promise(resolve => setTimeout(resolve, 1500))

      try {
        await paymentAPI.sandboxPayBooking(result.order_id)
        successVisible.value = true
        if (timer) clearInterval(timer)
        ElMessage.success('支付成功！')
      } catch (err: any) {
        ElMessage.error(err?.response?.data?.detail || '支付确认失败')
      }
    }
  } catch (err: any) {
    console.error('预订支付失败:', err)
    ElMessage.error(err?.response?.data?.detail || '创建支付订单失败，请重试')
  } finally {
    paying.value = false
  }
}

function handleFindAlternative(item: any) {
  ElMessage.info(`正在为「${item.name}」查找备选方案...`)
}

onMounted(async () => {
  // 检查是否从支付宝支付页面返回
  const paid = route.query.paid
  if (paid === '1') {
    successVisible.value = true
    if (timer) clearInterval(timer)
    // 清除 URL 参数
    router.replace('/itinerary/payment')
    return
  }

  timer = setInterval(() => {
    remaining.value = Math.max(0, remaining.value - 1)
  }, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped lang="scss">
.payment-view {
  min-height: calc(100vh - 64px);
  background: var(--color-bg);
  padding: var(--space-xl) var(--space-lg);
}

.payment-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: var(--space-xl);
}

// Left: Booking
.booking-section {
  flex: 1.2;
  min-width: 0;
}

.section-header {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  margin-bottom: var(--space-lg);

  h3 { font-size: var(--font-size-lg); font-weight: 700; }
}

.booking-group {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
  margin-bottom: var(--space-md);
  overflow: hidden;
}

.group-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md) var(--space-lg);
  cursor: pointer;
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
  transition: background var(--transition-fast);

  &:hover { background: var(--color-bg); }
}

.group-label { flex: 1; }
.group-count { color: var(--color-text-muted); font-weight: 400; }
.group-total { color: var(--color-primary); font-weight: 700; }

.group-items {
  padding: 0 var(--space-lg) var(--space-md);
}

// Right: Payment
.payment-section {
  width: 380px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

// Success dialog
.success-content {
  text-align: center;
  padding: var(--space-lg) 0;

  .success-icon {
    color: var(--color-success);
    margin-bottom: var(--space-md);
  }

  h3 { font-size: var(--font-size-xl); font-weight: 700; margin-bottom: var(--space-sm); }
  p { color: var(--color-text-secondary); margin-bottom: var(--space-lg); }
}

.success-actions {
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .payment-container { flex-direction: column; }
  .payment-section { width: 100%; }
}
</style>
