<template>
  <div class="itineraries-view">
    <div class="view-header">
      <h3>我的行程</h3>
      <button class="ai-generate-btn" @click="$router.push('/itinerary/generate')">
        <span class="btn-icon-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L12 6"/><path d="M12 18L12 22"/><path d="M4.93 4.93L7.76 7.76"/><path d="M16.24 16.24L19.07 19.07"/><path d="M2 12L6 12"/><path d="M18 12L22 12"/><path d="M4.93 19.07L7.76 16.24"/><path d="M16.24 7.76L19.07 4.93"/></svg>
        </span>
        <span class="btn-text">AI 生成新行程</span>
      </button>
    </div>

    <!-- Loading -->
    <el-skeleton v-if="loading" :rows="4" animated />

    <!-- Empty -->
    <el-empty
      v-else-if="itineraryList.length === 0"
      description="还没有行程，让 AI 帮你规划一次旅行吧！"
    >
      <button class="ai-generate-btn" @click="$router.push('/itinerary/generate')">
        开始规划
      </button>
    </el-empty>

    <!-- List -->
    <div v-else class="itinerary-grid">
      <div
        v-for="item in itineraryList"
        :key="item.id"
        class="itinerary-card card-lift"
        @click="$router.push(`/itinerary/${item.id}`)"
      >
        <div class="card-cover" :style="{ background: coverGradient(item.destination) }">
          <img class="cover-image" :src="coverImage(item.destination)" :alt="item.destination" />
          <el-tag
            :type="statusTagType(item.status)"
            size="small"
            effect="dark"
            round
            class="cover-tag"
          >
            {{ statusLabel(item.status) }}
          </el-tag>
        </div>

        <div class="card-body">
          <h4 class="card-title">{{ item.title }}</h4>
          <div class="card-meta">
            <div class="meta-row">
              <el-icon :size="14"><Location /></el-icon>
              <span>{{ item.destination }}</span>
            </div>
            <div class="meta-row" v-if="item.start_date">
              <el-icon :size="14"><Calendar /></el-icon>
              <span>{{ item.start_date }} ~ {{ item.end_date }}</span>
            </div>
            <div class="meta-row" v-if="item.total_budget">
              <el-icon :size="14"><Money /></el-icon>
              <span class="price-text">¥{{ (item.total_budget || 0).toLocaleString() }}</span>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <span class="footer-date">{{ formatDate(item.created_at) }}</span>
          <el-button type="danger" size="small" text @click.stop="handleDelete(item.id)">
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
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
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useItineraryStore } from '@/stores/itinerary'
import { useUserStore } from '@/stores/user'
import type { ItineraryResponse } from '@/types/itinerary'
import { Location, Calendar, Money, Delete } from '@element-plus/icons-vue'

const itineraryStore = useItineraryStore()
const userStore = useUserStore()

const loading = ref(false)
const itineraryList = ref<ItineraryResponse[]>([])
const currentPage = ref(1)
const pageSize = 10
const total = ref(0)

const destGradients: Record<string, { emoji: string; gradient: string; image: string }> = {
  '北京': { emoji: '🏯', gradient: 'linear-gradient(135deg, #E17055, #F7A800)', image: '/assets/destinations/beijing.png' },
  '成都': { emoji: '🐼', gradient: 'linear-gradient(135deg, #00B894, #0D7377)', image: '/assets/destinations/chengdu.png' },
  '上海': { emoji: '🌃', gradient: 'linear-gradient(135deg, #6C5CE7, #74B9FF)', image: '/assets/destinations/shanghai.png' },
  '云南': { emoji: '🏔️', gradient: 'linear-gradient(135deg, #FF6B35, #E17055)', image: '/assets/destinations/yunnan.png' },
  '三亚': { emoji: '🏖️', gradient: 'linear-gradient(135deg, #0984E3, #00CEC9)', image: '/assets/destinations/sanya.png' },
  '西安': { emoji: '🏛️', gradient: 'linear-gradient(135deg, #D63031, #E17055)', image: '/assets/destinations/xian.png' },
}

function coverGradient(dest: string) {
  return destGradients[dest]?.gradient || 'var(--gradient-hero)'
}

function coverEmoji(dest: string) {
  return destGradients[dest]?.emoji || '📍'
}

function coverImage(dest: string) {
  return destGradients[dest]?.image || '/assets/destinations/beijing.png'
}

const statusLabel = (s: string) => {
  const map: Record<string, string> = { draft: '草稿', planned: '已规划', in_progress: '进行中', completed: '已完成', cancelled: '已取消' }
  return map[s] || s
}

const statusTagType = (s: string): 'info' | 'success' | 'warning' | 'danger' => {
  const map: Record<string, 'info' | 'success' | 'warning' | 'danger'> = { draft: 'info', planned: 'warning', in_progress: 'success', completed: 'success', cancelled: 'danger' }
  return map[s] || 'info'
}

const formatDate = (d: string) => d ? new Date(d).toLocaleDateString('zh-CN') : ''

async function loadItineraries() {
  if (!userStore.user?.id) return
  loading.value = true
  try {
    const result = await itineraryStore.fetchItineraries(userStore.user.id, currentPage.value, pageSize)
    itineraryList.value = result.items
    total.value = result.total
  } catch {
    ElMessage.error('加载行程列表失败')
  } finally {
    loading.value = false
  }
}

function handlePageChange(page: number) { currentPage.value = page; loadItineraries() }

async function handleDelete(id: string) {
  try {
    await ElMessageBox.confirm('确定要删除这个行程吗？', '确认删除', { confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning' })
    await itineraryStore.deleteItinerary(id)
    itineraryList.value = itineraryList.value.filter(it => it.id !== id)
    ElMessage.success('行程已删除')
  } catch { /* cancelled */ }
}

onMounted(() => { loadItineraries() })
</script>

<style scoped lang="scss">
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-xl);

  h3 { font-size: var(--font-size-lg); font-weight: 700; margin: 0; }
}

// AI 生成按钮 — 暗色主题适配
.ai-generate-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: #1a1a1a;
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.25s ease;
  box-shadow: 0 2px 12px rgba(245, 158, 11, 0.3);
  white-space: nowrap;

  .btn-icon-wrap {
    display: flex;
    align-items: center;
    justify-content: center;

    svg {
      width: 16px;
      height: 16px;
    }
  }

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 18px rgba(245, 158, 11, 0.45);
    filter: brightness(1.08);
  }

  &:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.25);
  }
}

.itinerary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-lg);
}

.itinerary-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
  cursor: pointer;
}

.card-cover {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.cover-image {
  width: 64px; height: 64px;
  border-radius: 16px; object-fit: cover;
  flex-shrink: 0;
  filter: drop-shadow(0 4px 12px rgba(0,0,0,0.3));
}

.cover-tag {
  position: absolute;
  top: 10px;
  right: 10px;
}

.card-body {
  padding: var(--space-md);
}

.card-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-sm);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);

  .price-text {
    color: var(--color-primary);
    font-weight: 600;
  }
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-sm) var(--space-md);
  border-top: 1px solid var(--color-border-light);
}

.footer-date {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: var(--space-xl);
}
</style>
