<template>
  <div class="detail-view">
    <!-- Hero Banner -->
    <div class="detail-hero">
      <div class="hero-bg-pattern" />
      <div class="container hero-content">
        <button class="back-link" @click="$router.back()">
          <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd"/></svg>
          <span>返回</span>
        </button>

        <el-skeleton :loading="loading" animated>
          <template v-if="itinerary">
            <div class="hero-info">
              <div class="hero-badge-row">
                <el-tag :type="statusType" effect="dark" round size="small">
                  {{ statusLabel }}
                </el-tag>
                <span class="hero-version">v{{ itinerary.version }}</span>
              </div>
              <h1 class="hero-title">{{ itinerary.title }}</h1>
              <div class="hero-meta">
                <div class="hero-meta-item">
                  <el-icon :size="18"><LocationFilled /></el-icon>
                  <span>{{ itinerary.destination }}</span>
                </div>
                <div class="hero-meta-item">
                  <el-icon :size="18"><Calendar /></el-icon>
                  <span>{{ itinerary.start_date || '待定' }} ~ {{ itinerary.end_date || '待定' }}</span>
                </div>
                <div class="hero-meta-item price">
                  <el-icon :size="18"><Money /></el-icon>
                  <span>¥{{ (itinerary.total_budget || 0).toLocaleString() }}</span>
                </div>
              </div>
              <div class="hero-tags" v-if="itinerary.preferences?.length">
                <el-tag v-for="p in itinerary.preferences" :key="p" size="small" round>{{ p }}</el-tag>
              </div>
              <div class="hero-actions">
                <button class="hero-action-btn hero-action-edit" @click="$router.push(`/editor/${itinerary.id}`)">
                  <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/></svg>
                  编辑行程
                </button>
                <button class="hero-action-btn hero-action-regen" @click="$router.push('/itinerary/generate')">
                  <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/></svg>
                  重新生成
                </button>
              </div>
            </div>
          </template>
        </el-skeleton>
      </div>
    </div>

    <!-- Timeline Content -->
    <div class="container detail-body">
      <el-skeleton :loading="loading" animated :rows="5">
        <template v-if="itinerary">
          <div class="body-header">
            <SectionTitle overline="行程详情" size="sm" :no-line="true">
              每日安排
            </SectionTitle>
            <DayNavigator
              v-if="itinerary.days && itinerary.days.length > 1"
              v-model="activeDay"
              :days="itinerary.days"
            />
          </div>

          <BudgetBar v-if="itinerary.days" :days="itinerary.days" />

          <div class="detail-timeline">
            <TimelineDay
              v-if="itinerary.days && itinerary.days[activeDay]"
              :day="itinerary.days[activeDay]"
            />
          </div>
        </template>
      </el-skeleton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useItineraryStore } from '@/stores/itinerary'
import type { ItineraryResponse } from '@/types/itinerary'
import TimelineDay from '@/components/itinerary/TimelineDay.vue'
import DayNavigator from '@/components/itinerary/DayNavigator.vue'
import BudgetBar from '@/components/itinerary/BudgetBar.vue'
import SectionTitle from '@/components/common/SectionTitle.vue'
import {
  LocationFilled, Calendar, Money,
} from '@element-plus/icons-vue'

const route = useRoute()
const store = useItineraryStore()
const itinerary = ref<ItineraryResponse | null>(null)
const loading = ref(false)
const activeDay = ref(0)

const statusLabel = computed(() => {
  const map: Record<string, string> = {
    draft: '草稿', planned: '已规划', in_progress: '进行中',
    completed: '已完成', cancelled: '已取消',
  }
  return map[itinerary.value?.status || ''] || itinerary.value?.status || ''
})

const statusType = computed(() => {
  const map: Record<string, string> = {
    draft: 'info', planned: 'warning', in_progress: 'success',
    completed: 'success', cancelled: 'danger',
  }
  return map[itinerary.value?.status || ''] || 'info'
})

onMounted(async () => {
  loading.value = true
  itinerary.value = await store.fetchItinerary(route.params.id as string)
  loading.value = false
})
</script>

<style scoped lang="scss">
.detail-view {
  padding-bottom: var(--space-4xl);
}

.detail-hero {
  position: relative;
  background: var(--gradient-dark);
  padding: var(--space-3xl) 0;
  overflow: hidden;

  .hero-bg-pattern {
    position: absolute;
    inset: 0;
    background:
      radial-gradient(ellipse 40% 60% at 80% 20%, rgba(255, 107, 53, 0.15), transparent),
      radial-gradient(ellipse 30% 40% at 20% 80%, rgba(247, 168, 0, 0.08), transparent);
  }
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
}

.hero-content {
  position: relative;
  z-index: 1;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.7);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  margin-bottom: var(--space-lg);
  transition: all 0.2s ease;

  svg { flex-shrink: 0; }

  &:hover {
    color: #fff;
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.22);
  }

  &:active {
    transform: scale(0.97);
  }
}

.hero-info {
  color: #fff;
}

.hero-badge-row {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-md);
}

.hero-version {
  font-size: var(--font-size-xs);
  color: rgba(255, 255, 255, 0.5);
}

.hero-title {
  font-size: var(--font-size-3xl);
  font-weight: 800;
  margin-bottom: var(--space-lg);
}

.hero-meta {
  display: flex;
  gap: var(--space-xl);
  margin-bottom: var(--space-lg);
  flex-wrap: wrap;
}

.hero-meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: var(--font-size-sm);
  color: rgba(255, 255, 255, 0.8);

  &.price {
    color: var(--color-accent-light);
    font-weight: 600;
  }
}

.hero-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: var(--space-xl);
}

.hero-actions {
  display: flex;
  gap: var(--space-md);
}

.hero-action-btn {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;

  svg { flex-shrink: 0; }
}

.hero-action-edit {
  border: none;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #0f172a;
  box-shadow: 0 2px 12px rgba(245, 158, 11, 0.3);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(245, 158, 11, 0.45);
  }

  &:active {
    transform: translateY(0);
  }
}

.hero-action-regen {
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.06);
  color: #e2e8f0;
  backdrop-filter: blur(4px);

  &:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.35);
    transform: translateY(-2px);
  }

  &:active {
    transform: translateY(0);
  }
}

.detail-body {
  padding-top: var(--space-xl);
}

.body-header {
  margin-bottom: var(--space-lg);
}

.detail-timeline {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  padding: var(--space-md);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: var(--font-size-2xl);
  }
  .hero-meta {
    gap: var(--space-md);
  }
  .hero-actions {
    flex-direction: column;
  }
}
</style>
