<template>
  <div class="editor-view">
    <!-- Top Toolbar -->
    <div class="editor-toolbar">
      <div class="toolbar-left">
        <div class="toolbar-info">
          <span class="toolbar-title" v-if="itinerary">{{ itinerary.title }}</span>
          <span class="toolbar-meta" v-if="itinerary">
            <span class="meta-dot">·</span>
            {{ currentDays.length }}天行程
            <span class="meta-dot">·</span>
            ¥{{ currentTotal.toLocaleString() }}
          </span>
        </div>
      </div>
      <div class="toolbar-center">
        <button class="toolbar-edit-btn" :disabled="undoStack.length === 0" @click="handleUndo" title="撤销">
          <svg viewBox="0 0 20 20" fill="currentColor" width="15" height="15"><path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd"/></svg>
          <span>撤销</span>
        </button>
        <button class="toolbar-edit-btn" :disabled="redoStack.length === 0" @click="handleRedo" title="重做">
          <svg viewBox="0 0 20 20" fill="currentColor" width="15" height="15"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
          <span>重做</span>
        </button>
      </div>
      <div class="toolbar-right">
        <button class="toolbar-cancel-btn" @click="$router.back()">取消</button>
        <button class="toolbar-save-btn" :disabled="saving" @click="handleSave">
          <svg v-if="!saving" viewBox="0 0 20 20" fill="currentColor" width="15" height="15"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
          <span v-if="saving" class="mini-spinner"></span>
          <span>{{ saving ? '保存中...' : '保存版本' }}</span>
        </button>
      </div>
    </div>

    <!-- Editor Body -->
    <div class="editor-body" v-loading="loading">
      <template v-if="itinerary">
        <div class="editor-layout">
          <!-- Left: Overview Panel -->
          <aside class="overview-panel">
            <!-- Stats -->
            <div class="overview-section">
              <h4 class="section-title">
                <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/></svg>
                行程概览
              </h4>

              <div class="stat-card">
                <div class="stat-icon days-icon">
                  <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/></svg>
                </div>
                <div class="stat-info">
                  <span class="stat-label">总天数</span>
                  <span class="stat-value">{{ currentDays.length }} 天</span>
                </div>
              </div>

              <div class="stat-card">
                <div class="stat-icon budget-icon">
                  <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z"/><path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd"/></svg>
                </div>
                <div class="stat-info">
                  <span class="stat-label">总预算</span>
                  <span class="stat-value budget-value" :style="{ color: budgetStatusColor() }">
                    ¥{{ currentTotal.toLocaleString() }}
                  </span>
                </div>
              </div>

              <div class="stat-card">
                <div class="stat-icon avg-icon">
                  <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clip-rule="evenodd"/></svg>
                </div>
                <div class="stat-info">
                  <span class="stat-label">日均预算</span>
                  <span class="stat-value">¥{{ avgPerDay.toLocaleString() }}</span>
                </div>
              </div>

              <!-- Budget progress bar -->
              <div v-if="itinerary?.budget" class="budget-meter">
                <div class="budget-meter-header">
                  <span>预算使用</span>
                  <span :style="{ color: budgetStatusColor() }">{{ budgetPercent }}%</span>
                </div>
                <div class="budget-meter-track">
                  <div
                    class="budget-meter-fill"
                    :style="{ width: budgetPercent + '%', background: budgetMeterGradient() }"
                  ></div>
                </div>
              </div>

              <div v-if="overBudget" class="budget-warning">
                <el-icon><WarningFilled /></el-icon>
                预算超支 ¥{{ overAmount.toLocaleString() }}
              </div>

              <div class="stat-card status-card">
                <div class="stat-icon status-icon" :class="'status-' + itinerary?.status">
                  <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/></svg>
                </div>
                <div class="stat-info">
                  <span class="stat-label">状态</span>
                  <el-tag :type="statusTagType(itinerary?.status || 'draft')" size="small" round>
                    {{ statusLabel(itinerary?.status || 'draft') }}
                  </el-tag>
                </div>
              </div>
            </div>

            <!-- Version Management -->
            <div class="overview-section">
              <h4 class="section-title">
                <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/></svg>
                版本管理
              </h4>
              <VersionSelector
                v-model="activeVersion"
                :versions="versionList"
              />
            </div>

            <!-- Actions -->
            <div class="overview-section">
              <h4 class="section-title">
                <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/></svg>
                操作
              </h4>
              <div class="action-buttons">
                <button class="editor-action-btn action-save" @click="handleSave">
                  <svg viewBox="0 0 20 20" fill="currentColor" width="15" height="15"><path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a2 2 0 012-2h8a2 2 0 012 2v12l-6-3-6 3V7z"/></svg>
                  <span>保存版本</span>
                </button>
                <button class="editor-action-btn action-book" @click="goToPayment">
                  <svg viewBox="0 0 20 20" fill="currentColor" width="15" height="15"><path fill-rule="evenodd" d="M12 1.586l-4 4V6h8v3h2V6a2 2 0 00-2-2h-4V1.586zM3 3a2 2 0 00-2 2v12a2 2 0 002 2h4v-2H3V5h9v3h3v3h2V8.586l-2-2V5.414l-2-2V5H3v8h1v2H3z" clip-rule="evenodd"/><path d="M13 13a2 2 0 012-2h3a2 2 0 012 2v4a1 1 0 01-1 1h-5a1 1 0 01-1-1v-4z"/></svg>
                  <span>一键预订</span>
                </button>
                <button class="editor-action-btn action-share">
                  <svg viewBox="0 0 20 20" fill="currentColor" width="15" height="15"><path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.03 3.03 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z"/></svg>
                  <span>分享行程</span>
                </button>
              </div>
            </div>
          </aside>

          <!-- Right: Timeline -->
          <main class="timeline-panel">
            <div class="day-columns">
              <div
                v-for="(day, dayIndex) in currentDays"
                :key="day.day_index"
                class="day-column"
              >
                <div class="column-header">
                  <div class="column-title">
                    <span class="column-day-badge">Day {{ day.day_index }}</span>
                    <span v-if="day.date" class="column-date">{{ day.date }}</span>
                    <span class="column-weather" v-if="day.date">
                      <svg viewBox="0 0 20 20" fill="currentColor" width="13" height="13"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9z" clip-rule="evenodd"/></svg>
                      22°C
                    </span>
                  </div>
                  <el-button text size="small" class="column-add-btn" @click="addActivity(dayIndex)" title="添加活动">
                    <el-icon><Plus /></el-icon>
                    <span>添加</span>
                  </el-button>
                </div>

                <div class="column-activities">
                  <draggable
                    v-model="day.activities"
                    :group="'itinerary-days'"
                    item-key="id"
                    handle=".drag-handle"
                    :animation="200"
                    ghost-class="sortable-ghost"
                    drag-class="sortable-drag"
                    chosen-class="sortable-chosen"
                    @change="onDragChange"
                  >
                    <template #item="{ element: activity }">
                      <DragActivity
                        :activity="activity"
                        @edit="openDrawer($event)"
                        @replace="openDrawer($event)"
                        @delete="removeActivityByRef(dayIndex, activity)"
                      />
                    </template>
                  </draggable>
                </div>

                <!-- Hotel slot — outside scrollable area, fixed at column bottom -->
                <div v-if="day.hotel" class="hotel-slot">
                  <div class="hotel-label">
                    <el-icon><Moon /></el-icon>
                    <span>住宿</span>
                  </div>
                  <DragActivity
                    :activity="day.hotel"
                    @edit="openDrawer($event)"
                    @replace="openDrawer($event)"
                    @delete="removeHotel(dayIndex)"
                  />
                </div>
                <div v-else class="hotel-slot hotel-slot-empty">
                  <button class="add-hotel-btn" @click="addHotel(dayIndex)">
                    <div class="add-hotel-icon">
                      <svg viewBox="0 0 20 20" fill="currentColor" width="18" height="18"><path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/></svg>
                    </div>
                    <span>添加住宿</span>
                  </button>
                </div>
              </div>
            </div>
          </main>
        </div>
      </template>

      <el-empty v-else-if="!loading" description="加载行程数据失败">
        <button class="sidebar-action-btn sidebar-action-save" @click="$router.back()">返回</button>
      </el-empty>
    </div>

    <!-- Activity Drawer -->
    <ActivityDrawer
      v-model:visible="drawerVisible"
      :activity="editingActivity"
      @save="handleActivitySave"
      @replace="handleActivityReplace"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useItineraryEdit } from '@/composables/useItineraryEdit'
import { useBudget } from '@/composables/useBudget'
import { useItineraryStore } from '@/stores/itinerary'
import type { ItineraryResponse, DayItinerary, ActivityItem } from '@/types/itinerary'
import DragActivity from '@/components/itinerary/DragActivity.vue'
import VersionSelector from '@/components/itinerary/VersionSelector.vue'
import ActivityDrawer from '@/components/itinerary/ActivityDrawer.vue'
import draggable from 'vuedraggable'
import {
  Plus, Moon, WarningFilled,
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const itineraryStore = useItineraryStore()
const { undoStack, redoStack, undo, redo, addActivity: editAddActivity, removeActivity: editRemoveActivity } = useItineraryEdit()

const itinerary = ref<ItineraryResponse | null>(null)
const currentDays = ref<DayItinerary[]>([])
const loading = ref(false)
const saving = ref(false)

const { currentTotal, avgPerDay, overBudget, overAmount, checkBudget, budgetStatusColor } = useBudget(currentDays)

// Drawer state
const drawerVisible = ref(false)
const editingActivity = ref<ActivityItem | null>(null)

// Version state
const activeVersion = ref(1)
const versionList = ref<{ version: number; created_at: string; summary: string }[]>([])

const statusLabel = (s: string) => ({ draft: '草稿', planned: '已规划', in_progress: '进行中', completed: '已完成', cancelled: '已取消' } as Record<string, string>)[s] || s
const statusTagType = (s: string): 'info' | 'success' | 'warning' | 'danger' => ({ draft: 'info', planned: 'warning', in_progress: 'success', completed: 'success', cancelled: 'danger' } as any)[s] || 'info'

// Budget meter
const budgetPercent = computed(() => {
  if (!itinerary.value?.budget || itinerary.value.budget <= 0) return 0
  return Math.min(100, Math.round((currentTotal.value / itinerary.value.budget) * 100))
})
const budgetMeterGradient = () => {
  const p = budgetPercent.value
  if (p > 100) return 'linear-gradient(90deg, #ef4444, #f87171)'
  if (p > 80) return 'linear-gradient(90deg, #f59e0b, #fbbf24)'
  return 'linear-gradient(90deg, #10b981, #34d399)'
}

onMounted(async () => {
  loading.value = true
  const result = await itineraryStore.fetchItinerary(route.params.id as string)
  if (result) {
    itinerary.value = result
    currentDays.value = JSON.parse(JSON.stringify(result.days || []))
    activeVersion.value = result.version || 1
    versionList.value = [{ version: result.version || 1, created_at: result.updated_at || '', summary: '当前版本' }]
    checkBudget()
  }
  loading.value = false
})

function addActivity(dayIndex: number) {
  editingActivity.value = null
  drawerVisible.value = true
}

function removeActivityByRef(dayIndex: number, target: ActivityItem) {
  const day = currentDays.value[dayIndex]
  if (!day) return
  const idx = day.activities.findIndex(a => a.id === target.id)
  if (idx >= 0) {
    currentDays.value = editRemoveActivity(currentDays.value, dayIndex, idx)
    checkBudget()
  }
}

function removeActivity(dayIndex: number, actIndex: number) {
  currentDays.value = editRemoveActivity(currentDays.value, dayIndex, actIndex)
  checkBudget()
}

// vuedraggable change handler
function onDragChange() {
  // SortableJS already mutates the array via v-model, just recalculate budget
  checkBudget()
}

function addHotel(dayIndex: number) {
  const hotel: ActivityItem = {
    id: `hotel-${Date.now()}`, type: 'hotel', name: '新酒店', description: '',
    address: '', lat: 0, lng: 0, start_time: '', end_time: '', price: 0, tags: [], notes: '',
  }
  currentDays.value[dayIndex].hotel = hotel
  checkBudget()
}

function removeHotel(dayIndex: number) {
  currentDays.value[dayIndex].hotel = null
  checkBudget()
}

function openDrawer(activity: ActivityItem) {
  editingActivity.value = activity
  drawerVisible.value = true
}

function handleActivitySave(activity: ActivityItem) {
  // Find and update or add activity
  // Simplified: add to first day
  if (currentDays.value.length > 0) {
    const existingIdx = currentDays.value[0].activities.findIndex(a => a.id === activity.id)
    if (existingIdx >= 0) {
      currentDays.value[0].activities[existingIdx] = activity
    } else {
      currentDays.value[0].activities.push(activity)
    }
  }
  checkBudget()
}

function handleActivityReplace(oldAct: ActivityItem, newAct: ActivityItem) {
  for (const day of currentDays.value) {
    const idx = day.activities.findIndex(a => a.id === oldAct.id)
    if (idx >= 0) {
      day.activities[idx] = { ...day.activities[idx], ...newAct }
      break
    }
  }
  checkBudget()
}

async function handleSave() {
  const id = route.params.id as string
  if (!id || currentDays.value.length === 0) {
    ElMessage.warning('没有可保存的行程数据')
    return
  }
  saving.value = true
  try {
    await itineraryStore.updateItinerary(id, { days: currentDays.value })
    versionList.value.unshift({ version: (activeVersion.value + 1), created_at: new Date().toISOString(), summary: '手动保存' })
    activeVersion.value++
    ElMessage.success('版本已保存')
  } catch {
    ElMessage.error('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

function handleUndo() {
  const prev = undo(currentDays.value)
  if (prev) currentDays.value = prev
}

function handleRedo() {
  const next = redo(currentDays.value)
  if (next) currentDays.value = next
}

function goToPayment() {
  router.push({ name: 'payment', params: { orderId: route.params.id } })
}
</script>

<style scoped lang="scss">
// ───────────────────────────────────
// Editor View — Layout
// ───────────────────────────────────
.editor-view {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.editor-body {
  flex: 1;
  overflow: hidden;
}

.editor-layout {
  display: flex;
  height: 100%;
}

// ───────────────────────────────────
// Toolbar
// ───────────────────────────────────
.editor-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-lg);
  height: 52px;
  background: linear-gradient(180deg, rgba(17, 24, 39, 0.95), rgba(17, 24, 39, 0.85));
  border-bottom: 1px solid var(--color-border-light);
  flex-shrink: 0;
  gap: var(--space-md);
  backdrop-filter: blur(8px);
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  min-width: 0;
  flex: 1;
}

.toolbar-info {
  display: flex;
  align-items: baseline;
  gap: var(--space-sm);
  min-width: 0;
}

.toolbar-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-primary);
  max-width: 260px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.toolbar-meta {
  font-size: 11px;
  color: var(--color-text-muted);
  white-space: nowrap;
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.meta-dot {
  color: #475569;
  font-weight: 700;
}

.toolbar-center {
  display: flex;
  gap: 2px;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 10px;
  padding: 3px;
  flex-shrink: 0;
}

.toolbar-edit-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #94a3b8;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  svg { flex-shrink: 0; }

  &:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.08);
    color: #e2e8f0;
  }

  &:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }
}

.toolbar-right {
  display: flex;
  gap: var(--space-sm);
  flex-shrink: 0;
}

.toolbar-cancel-btn {
  padding: 6px 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 9px;
  background: transparent;
  color: #94a3b8;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    border-color: rgba(255, 255, 255, 0.2);
    color: #e2e8f0;
    background: rgba(255, 255, 255, 0.04);
  }
}

.toolbar-save-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 16px;
  border: none;
  border-radius: 9px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #0f172a;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);

  svg { flex-shrink: 0; }

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(245, 158, 11, 0.35);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
}

.mini-spinner {
  display: inline-block;
  width: 13px;
  height: 13px;
  border: 2px solid rgba(15, 23, 42, 0.3);
  border-top-color: #0f172a;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

// ───────────────────────────────────
// Overview Panel (Sidebar)
// ───────────────────────────────────
.overview-panel {
  width: 250px;
  flex-shrink: 0;
  border-right: 1px solid var(--color-border-light);
  padding: var(--space-lg);
  overflow-y: auto;
  background: var(--color-bg);
  display: flex;
  flex-direction: column;
  gap: 0;
}

.overview-section {
  margin-bottom: var(--space-xl);

  &:last-child { margin-bottom: 0; }
}

.section-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: var(--color-text-muted);
  margin-bottom: var(--space-md);

  svg { opacity: 0.6; flex-shrink: 0; }
}

// Stat cards
.stat-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  border-radius: 10px;
  margin-bottom: 8px;
  transition: all 0.2s ease;

  &:hover {
    border-color: rgba(255, 255, 255, 0.1);
  }
}

.stat-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #fff;
}

.days-icon { background: linear-gradient(135deg, #3b82f6, #60a5fa); }
.budget-icon { background: linear-gradient(135deg, #f59e0b, #fbbf24); }
.avg-icon { background: linear-gradient(135deg, #8b5cf6, #a78bfa); }
.status-icon {
  background: #334155;
  &.status-draft { background: #475569; }
  &.status-planned { background: linear-gradient(135deg, #f59e0b, #d97706); }
  &.status-in_progress { background: linear-gradient(135deg, #10b981, #059669); }
  &.status-completed { background: linear-gradient(135deg, #3b82f6, #2563eb); }
  &.status-cancelled { background: linear-gradient(135deg, #ef4444, #dc2626); }
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;

  .stat-label {
    font-size: 11px;
    color: var(--color-text-muted);
  }

  .stat-value {
    font-size: 14px;
    font-weight: 700;
    color: var(--color-text-primary);
  }
}

.budget-value { font-weight: 700; }

.status-card {
  margin-top: 8px;
}

// Budget meter
.budget-meter {
  margin-bottom: 8px;
  padding: 0 2px;
}

.budget-meter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  font-size: 11px;

  span:first-child { color: var(--color-text-muted); }
  span:last-child { font-weight: 600; font-size: 12px; }
}

.budget-meter-track {
  width: 100%;
  height: 5px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 3px;
  overflow: hidden;
}

.budget-meter-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

// Budget warning
.budget-warning {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: var(--color-warning-light);
  color: var(--color-warning);
  font-size: 11px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  margin-top: 4px;
  margin-bottom: 8px;
}

// Action buttons
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.editor-action-btn {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 10px 14px;
  border: none;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.22s ease;
  width: 100%;

  svg { flex-shrink: 0; opacity: 0.85; }
}

.action-save {
  background: rgba(255, 255, 255, 0.05);
  color: #e2e8f0;
  border: 1px solid rgba(255, 255, 255, 0.08);

  &:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.15);
    transform: translateY(-1px);
  }
}

.action-book {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #0f172a;
  box-shadow: 0 2px 10px rgba(245, 158, 11, 0.2);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 18px rgba(245, 158, 11, 0.35);
  }

  &:active { transform: translateY(0); }
}

.action-share {
  background: transparent;
  color: #94a3b8;
  border: 1px solid rgba(255, 255, 255, 0.06);

  &:hover {
    color: #e2e8f0;
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.12);
  }
}

// ───────────────────────────────────
// Timeline Panel
// ───────────────────────────────────
.timeline-panel {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  padding: var(--space-lg);
  background: linear-gradient(180deg, var(--color-bg) 0%, #080c16 100%);
}

.day-columns {
  display: flex;
  gap: var(--space-lg);
  height: 100%;
  min-width: max-content;
}

.day-column {
  width: 340px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border-radius: 14px;
  border: 1px solid var(--color-border-light);
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
  transition: box-shadow 0.3s ease;

  &:hover {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
  }
}

.column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border-light);
  background: rgba(255, 255, 255, 0.015);
}

.column-title {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.column-day-badge {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-primary);
  background: rgba(245, 158, 11, 0.1);
  padding: 2px 8px;
  border-radius: 5px;
  white-space: nowrap;
}

.column-date {
  font-size: 11px;
  color: var(--color-text-secondary);
  white-space: nowrap;
}

.column-weather {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  color: var(--color-info);
  white-space: nowrap;

  svg { flex-shrink: 0; opacity: 0.7; }
}

.column-add-btn {
  display: flex;
  align-items: center;
  gap: 3px !important;
  padding: 4px 10px !important;
  border-radius: 7px !important;
  color: var(--color-text-secondary) !important;
  font-size: 11px !important;
  font-weight: 500;
  transition: all 0.2s ease;

  &:hover {
    color: var(--color-primary) !important;
    background: rgba(245, 158, 11, 0.08) !important;
  }
}

// Activity area — scrollable, fills remaining column space
.column-activities {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;

  // Ensure empty draggable container is still a valid drop target
  > :deep(div) {
    min-height: 50px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  // Scrollbar styling
  &::-webkit-scrollbar { width: 4px; }
  &::-webkit-scrollbar-track { background: transparent; }
  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 2px;
  }
}

// Hotel slot — fixed at column bottom, outside scrollable area
.hotel-slot {
  flex-shrink: 0;
  padding: 10px 12px 12px;
  border-top: 1px dashed rgba(255, 255, 255, 0.08);
}

.hotel-slot-empty {
  display: flex;
  justify-content: center;
  padding-top: 6px;
  padding-bottom: 14px;
  border-top: 1px dashed rgba(255, 255, 255, 0.06);
}

.hotel-label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  color: var(--color-warning);
  margin-bottom: 8px;

  .el-icon { font-size: 13px; }
}

.add-hotel-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 7px;
  width: 100%;
  min-height: 72px;
  padding: 14px 12px;
  border: 2px dashed rgba(245, 158, 11, 0.2);
  border-radius: 12px;
  background: rgba(245, 158, 11, 0.03);
  color: #f59e0b;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;

  &:hover {
    border-color: rgba(245, 158, 11, 0.5);
    background: rgba(245, 158, 11, 0.07);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.12);
  }

  &:active { transform: translateY(0); }
}

.add-hotel-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(245, 158, 11, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;

  .add-hotel-btn:hover & {
    background: rgba(245, 158, 11, 0.25);
    transform: scale(1.1);
  }

  svg { opacity: 0.8; }
}

// ───────────────────────────────────
// Responsive
// ───────────────────────────────────
@media (max-width: 768px) {
  .toolbar-center { display: none; }
  .toolbar-meta { display: none; }
  .overview-panel { display: none; }
  .day-column { width: 280px; }
}
</style>
