<template>
  <div class="orders-view">
    <div class="view-header">
      <h3>我的订单</h3>
    </div>

    <el-skeleton v-if="loading" :rows="3" animated />

    <div v-else-if="orderList.length === 0" class="empty-state">
      <div class="empty-icon-wrap">
        <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="12" y="20" width="56" height="44" rx="6" stroke="#334155" stroke-width="2.5"/>
          <path d="M28 32h24M28 40h16M28 48h10" stroke="#475569" stroke-width="2" stroke-linecap="round"/>
          <circle cx="58" cy="58" r="14" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
          <path d="M54 58l3 3 5-5" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <p class="empty-text">暂无订单，快去预订行程中的酒店和门票吧！</p>
    </div>

    <div v-else class="order-list">
      <div v-for="order in orderList" :key="order.id" class="order-card">
        <div class="order-header">
          <div class="order-id">订单号: {{ order.id.slice(0, 14) }}...</div>
          <el-tag :type="orderStatusTag(order.status)" size="small" round effect="dark">
            {{ orderStatusLabel(order.status) }}
          </el-tag>
        </div>

        <div class="order-items">
          <div v-for="(item, idx) in order.items" :key="idx" class="order-item">
            <span class="item-type-tag" :class="item.resource_type">
              {{ itemTypeLabel(item.resource_type) }}
            </span>
            <span class="item-name">{{ item.name }}</span>
            <span class="item-qty">×{{ item.quantity }}</span>
            <span class="item-price">¥{{ item.price }}</span>
          </div>
        </div>

        <div class="order-footer">
          <div class="footer-left">
            <span class="total-label">合计</span>
            <span class="total-amount">¥{{ order.total_amount }}</span>
          </div>

          <CountdownTimer
            v-if="order.status === 'pending' && order.expire_at && calcRemaining(order.expire_at) > 0"
            :remaining="calcRemaining(order.expire_at)"
          />
        </div>

        <div class="order-actions" v-if="order.status === 'pending'">
          <el-button size="small" plain type="danger" @click="handleCancel(order)">取消</el-button>
          <el-button size="small" type="primary" @click="handlePay(order)">立即支付</el-button>
        </div>

        <div class="order-time">{{ formatDate(order.created_at) }}</div>
      </div>
    </div>

    <div class="pagination" v-if="total > pageSize">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        background
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { paymentAPI } from '@/api/payment'
import CountdownTimer from '@/components/payment/CountdownTimer.vue'

const userStore = useUserStore()

const loading = ref(false)
const orderList = ref<any[]>([])
const currentPage = ref(1)
const pageSize = 10
const total = ref(0)
let timer: ReturnType<typeof setInterval> | null = null

const orderStatusLabel = (s: string) => ({ pending: '待支付', paid: '已支付', timeout: '已过期', cancelled: '已取消', refunded: '已退款' } as Record<string, string>)[s] || s
const orderStatusTag = (s: string): 'warning' | 'success' | 'info' | 'danger' => ({ pending: 'warning', paid: 'success', timeout: 'info', cancelled: 'info', refunded: 'danger' } as any)[s] || 'info'
const itemTypeLabel = (t: string) => ({ hotel: '酒店', ticket: '门票', flight: '机票', restaurant: '餐厅', insurance: '保险' } as Record<string, string>)[t] || t
const formatDate = (d: string) => d ? new Date(d).toLocaleDateString('zh-CN') : ''
const calcRemaining = (expireAt: number | null | undefined) => {
  if (!expireAt) return 0
  return Math.max(0, expireAt - Math.floor(Date.now() / 1000))
}

async function loadOrders() {
  if (!userStore.user?.id) return
  loading.value = true
  try {
    const { data } = await paymentAPI.listOrders(userStore.user.id, currentPage.value, pageSize)
    const result = data.data
    if (result && typeof result === 'object') { orderList.value = result.items || []; total.value = result.total || 0 }
  } catch { ElMessage.error('加载订单列表失败') } finally { loading.value = false }
}

function handlePageChange(p: number) { currentPage.value = p; loadOrders() }

async function handlePay(order: any) {
  try {
    await ElMessageBox.confirm(`确认支付 ¥${order.total_amount}？`, '确认支付', { confirmButtonText: '支付', cancelButtonText: '取消', type: 'info' })
    await paymentAPI.pay(order.id, 'wechat' as any)
    ElMessage.success('支付成功！')
    loadOrders()
  } catch { /* cancelled */ }
}

async function handleCancel(order: any) {
  try {
    await ElMessageBox.confirm('确定要取消这个订单吗？', '取消订单', { confirmButtonText: '确认取消', cancelButtonText: '返回', type: 'warning' })
    await paymentAPI.cancelOrder(order.id)
    ElMessage.info('订单已取消')
    loadOrders()
  } catch { /* cancelled */ }
}

onMounted(() => {
  loadOrders()
  timer = setInterval(() => {
    const expired = orderList.value.some((o: any) => o.status === 'pending' && o.expire_at && calcRemaining(o.expire_at) === 0)
    if (expired) loadOrders()
  }, 5000)
})

onUnmounted(() => { if (timer) clearInterval(timer) })
</script>

<style scoped lang="scss">
.view-header {
  margin-bottom: var(--space-xl);
  h3 { font-size: var(--font-size-lg); font-weight: 700; margin: 0; }
}

// 空状态 — 暗色主题适配
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 24px;
}

.empty-icon-wrap {
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-surface);
  border-radius: 50%;
  margin-bottom: 20px;

  svg {
    width: 48px;
    height: 48px;
  }
}

.empty-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  text-align: center;
  max-width: 300px;
  line-height: 1.6;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.order-card {
    background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  transition: box-shadow var(--transition-base);
  &:hover { box-shadow: var(--shadow-md); }

  // Fix el-pagination inside dark theme
  :deep(.el-pagination) {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
  }
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-md);
}

.order-id {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  font-family: monospace;
}

.order-items {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  padding: var(--space-md) 0;
  border-top: 1px solid var(--color-border-light);
  border-bottom: 1px solid var(--color-border-light);
  margin-bottom: var(--space-md);
}

.order-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: var(--font-size-sm);
}

.item-type-tag {
  font-size: 10px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  &.hotel { background: var(--color-primary-lighter); color: var(--color-primary); }
  &.ticket { background: var(--color-secondary-lighter); color: var(--color-secondary); }
  &.flight { background: var(--color-info-light); color: var(--color-info); }
  &.restaurant { background: var(--color-accent-lighter); color: var(--color-accent); }
}

.item-name { flex: 1; font-weight: 500; color: var(--color-text-primary); }
.item-qty { color: var(--color-text-muted); }
.item-price { font-weight: 600; color: var(--color-text-secondary); white-space: nowrap; }

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-md);
}

.footer-left {
  display: flex;
  align-items: baseline;
  gap: var(--space-sm);
}

.total-label { font-size: var(--font-size-sm); color: var(--color-text-secondary); }
.total-amount { font-size: var(--font-size-xl); font-weight: 800; color: var(--color-primary); }

.order-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-sm);
}

.order-time {
  margin-top: var(--space-sm);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: var(--space-xl);

  :deep(.el-pagination) {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    flex-wrap: nowrap !important;
    .el-pager {
      display: flex !important;
      flex-direction: row !important;
      align-items: center !important;
    }
  }
}
</style>
