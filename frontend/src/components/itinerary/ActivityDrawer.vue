<template>
  <el-dialog
    :model-value="visible"
    :title="''"
    fullscreen
    class="activity-dialog"
    @update:model-value="$emit('update:visible', $event)"
    :show-close="false"
    :close-on-click-modal="false"
    :destroy-on-close="true"
  >
    <!-- 自定义顶部栏 -->
    <div class="dialog-topbar">
      <div class="topbar-left">
        <span class="topbar-title">{{ isNew ? '新建活动' : '编辑活动' }}</span>
        <span class="topbar-subtitle">{{ typeLabel(form.type) }} · 填写活动详情</span>
      </div>
      <button class="topbar-close" @click="$emit('update:visible', false)">
        <svg viewBox="0 0 20 20" fill="currentColor" width="18" height="18"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
      </button>
    </div>

    <div class="dialog-body">
      <div class="form-container">
        <!-- 类型选择 — 上方突出区域 -->
        <div class="section-card type-section">
          <label class="section-label">活动类型</label>
          <div class="type-cards">
            <button
              v-for="opt in typeOptions" :key="opt.value"
              class="type-card"
              :class="{ active: form.type === opt.value, [`card-${opt.value}`]: true }"
              @click="form.type = opt.value"
            >
              <div class="tc-icon" :class="`tc-${opt.value}`">
                <img :src="`/assets/poi/type_${opt.value}.png`" class="tc-img" />
              </div>
              <span class="tc-label">{{ opt.label }}</span>
            </button>
          </div>
        </div>

        <!-- 基本信息 — 两列布局 -->
        <div class="form-two-col">
          <!-- 活动名称 -->
          <div class="section-card">
            <label class="section-label">活动名称</label>
            <div class="input-field">
              <svg class="input-prefix-icon" viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/></svg>
              <input v-model="form.name" placeholder="请输入活动名称" class="native-input" type="text" />
            </div>
          </div>

          <!-- 预算费用 -->
          <div class="section-card">
            <label class="section-label">预算费用（元）</label>
            <div class="price-field">
              <div class="price-prepend">¥</div>
              <input v-model.number="form.price" type="number" min="0" step="50" class="price-num" placeholder="0" />
              <div class="price-steppers">
                <button class="step-btn" @click="form.price = Math.max(0, (form.price||0) - 50)">
                  <svg viewBox="0 0 20 20" fill="currentColor" width="12" height="12"><path fill-rule="evenodd" d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z" clip-rule="evenodd"/></svg>
                </button>
                <button class="step-btn plus" @click="form.price = (form.price||0) + 50">
                  <svg viewBox="0 0 20 20" fill="currentColor" width="12" height="12"><path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/></svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 时间段 & 地址 — 两列 -->
        <div class="form-two-col">
          <!-- 时间段 -->
          <div class="section-card">
            <label class="section-label">时间段</label>
            <div class="time-row">
              <button class="time-trigger-btn" :class="{ active: currentPicker === 'start' }" @click="openPicker('start')">
                <svg class="tu-icon" viewBox="0 0 18 18" fill="currentColor" width="14" height="14"><path fill-rule="evenodd" d="M9 16.5a7.5 7.5 0 100-15 7.5 7.5 0 000 15zm.75-9a.75.75 0 10-1.5 0v3c0 .2.08.39.22.53l2.12 2.12a.75.75 0 001.06-1.06L9.75 10.2V7.5z" clip-rule="evenodd"/></svg>
                <span class="tu-text">{{ form.start_time || '开始' }}</span>
                <svg class="tu-chevron" viewBox="0 0 20 20" fill="currentColor" width="12" height="12"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
              </button>

              <span class="time-arrow">
                <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
              </span>

              <button class="time-trigger-btn" :class="{ active: currentPicker === 'end' }" @click="openPicker('end')">
                <svg class="tu-icon" viewBox="0 0 18 18" fill="currentColor" width="14" height="14"><path fill-rule="evenodd" d="M9 16.5a7.5 7.5 0 100-15 7.5 7.5 0 000 15zm.75-9a.75.75 0 10-1.5 0v3c0 .2.08.39.22.53l2.12 2.12a.75.75 0 001.06-1.06L9.75 10.2V7.5z" clip-rule="evenodd"/></svg>
                <span class="tu-text">{{ form.end_time || '结束' }}</span>
                <svg class="tu-chevron" viewBox="0 0 20 20" fill="currentColor" width="12" height="12"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
              </button>
            </div>
          </div>

          <!-- 地址 -->
          <div class="section-card">
            <label class="section-label">活动地址</label>
            <div class="input-field">
              <svg class="input-prefix-icon" viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
              <input v-model="form.address" placeholder="请输入活动地址" class="native-input" type="text" />
              <button class="map-fab" @click="showMap = true" title="地图选点">
                <svg viewBox="0 0 20 20" fill="currentColor" width="15" height="15"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
              </button>
            </div>
          </div>
        </div>

        <!-- 标签 & 备注 — 两列 -->
        <div class="form-two-col">
          <div class="section-card">
            <label class="section-label">标签</label>
            <div class="tags-box">
              <span v-for="tag in form.tags" :key="tag" class="tag-badge">
                {{ tag }}
                <button class="tag-x" @click="removeTag(tag)">&times;</button>
              </span>
              <input v-model="tagInput" placeholder="输入标签后按回车" class="tag-new-input" @keyup.enter="addTag" />
            </div>
          </div>

          <div class="section-card">
            <label class="section-label">备注</label>
            <textarea v-model="form.notes" placeholder="备注信息（可选）" class="native-textarea" rows="3"></textarea>
          </div>
        </div>

        <!-- AI 推荐备选 -->
        <div v-if="!isNew" class="section-card ai-section">
          <button class="ai-toggle" @click="showReplacements = !showReplacements">
            <div class="ai-toggle-left">
              <svg viewBox="0 0 20 20" fill="currentColor" width="15" height="15"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
              <span>AI 推荐备选</span>
            </div>
            <svg :class="{ flipped: showReplacements }" class="ai-chevron" viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
          </button>
          <div v-if="showReplacements" class="ai-list">
            <div v-for="(alt, i) in alternatives" :key="i" class="ai-item">
              <div class="ai-item-info">
                <div class="ai-item-name">{{ alt.name }}</div>
                <div class="ai-item-meta">
                  <span class="ai-item-stars">&#9733; {{ alt.rating }}</span>
                  <span class="ai-item-price">¥{{ alt.price }}</span>
                </div>
              </div>
              <button class="ai-replace-btn" @click="replace(alt)">替换</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部操作栏 -->
    <div class="dialog-bottombar">
      <button class="btn-cancel" @click="$emit('update:visible', false)">取消</button>
      <button class="btn-confirm" @click="handleSave">
        <svg viewBox="0 0 20 20" fill="currentColor" width="15" height="15"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
        {{ isNew ? '创建活动' : '保存修改' }}
      </button>
    </div>

    <MapPopup
      v-if="showMap"
      :lat="form.lat"
      :lng="form.lng"
      :name="form.name"
      @close="showMap = false"
      @select="onMapSelect"
    />
  </el-dialog>

  <!-- 时间选择器浮层 (Teleport to body) -->
  <Teleport to="body">
    <Transition name="tp-overlay">
      <div v-if="currentPicker" class="time-overlay" @click.self="closePicker">
        <div class="time-panel">
          <div class="tp-header">
            <span class="tp-title">{{ currentPicker === 'start' ? '选择开始时间' : '选择结束时间' }}</span>
            <button class="tp-close" @click="closePicker">
              <svg viewBox="0 0 20 20" fill="currentColor" width="18" height="18"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
            </button>
          </div>

          <!-- 预设时间 -->
          <div class="tp-presets-grid">
            <button
              v-for="t in timePresets" :key="t"
              class="tp-preset-chip"
              :class="{ active: currentPicker === 'start' ? form.start_time === t : form.end_time === t }"
              @click="applyPreset(t)"
            >{{ t }}</button>
          </div>

          <!-- 分隔 -->
          <div class="tp-divider"><span>自定义时间</span></div>

          <!-- 自定义时分 -->
          <div class="tp-custom">
            <div class="tp-custom-col">
              <label class="tp-custom-label">时</label>
              <div class="tp-spin">
                <button class="tp-spin-btn" @click="adjustHour(1)"><svg viewBox="0 0 20 20" width="14" height="14"><path fill="currentColor" d="M5.293 7.707L10 2.999l4.707 4.708a1 1 0 01-1.414 1.414L10 5.828l-3.293 3.293a1 1 0 01-1.414-1.414z"/></svg></button>
                <div class="tp-spin-val">{{ pad2(pickerH) }}</div>
                <button class="tp-spin-btn" @click="adjustHour(-1)"><svg viewBox="0 0 20 20" width="14" height="14"><path fill="currentColor" d="M14.707 12.293L10 17 5.293 12.293a1 1 0 111.414-1.414L10 14.171l3.293-3.293a1 1 0 011.414 1.414z"/></svg></button>
              </div>
            </div>
            <span class="tp-custom-sep">:</span>
            <div class="tp-custom-col">
              <label class="tp-custom-label">分</label>
              <div class="tp-spin">
                <button class="tp-spin-btn" @click="adjustMin(5)"><svg viewBox="0 0 20 20" width="14" height="14"><path fill="currentColor" d="M5.293 7.707L10 2.999l4.707 4.708a1 1 0 01-1.414 1.414L10 5.828l-3.293 3.293a1 1 0 01-1.414-1.414z"/></svg></button>
                <div class="tp-spin-val">{{ pad2(pickerM) }}</div>
                <button class="tp-spin-btn" @click="adjustMin(-5)"><svg viewBox="0 0 20 20" width="14" height="14"><path fill="currentColor" d="M14.707 12.293L10 17 5.293 12.293a1 1 0 111.414-1.414L10 14.171l3.293-3.293a1 1 0 011.414 1.414z"/></svg></button>
              </div>
            </div>
          </div>

          <!-- 快捷预设 -->
          <div class="tp-quick-row">
            <button v-for="q in quickTimes" :key="q.label" class="tp-quick-btn" @click="applyPreset(q.value)">{{ q.label }}</button>
          </div>

          <button class="tp-confirm" @click="confirmPicker">确定</button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted, onUnmounted, nextTick, computed, type Ref } from 'vue'
import type { ActivityItem } from '@/types/itinerary'
import MapPopup from './MapPopup.vue'

const props = defineProps<{
  visible: boolean
  activity?: ActivityItem | null
}>()

const emit = defineEmits<{
  'update:visible': [boolean]
  save: [activity: ActivityItem]
  replace: [old: ActivityItem, newActivity: ActivityItem]
}>()

const isNew = ref(!props.activity)

const typeOptions = [
  { value: 'attraction', label: '景点' },
  { value: 'restaurant', label: '餐饮' },
  { value: 'hotel', label: '酒店' },
  { value: 'transport', label: '交通' },
]

function typeLabel(t: string) {
  return typeOptions.find(o => o.value === t)?.label || '活动'
}

const form = reactive<ActivityItem>({
  id: '',
  type: 'attraction',
  name: '',
  description: '',
  address: '',
  lat: 0,
  lng: 0,
  start_time: '09:00',
  end_time: '10:00',
  price: 0,
  tags: [],
  notes: '',
})

const tagInput = ref('')
const showMap = ref(false)
const showReplacements = ref(false)

// ── 高级时间选择器（居中浮层） ──
const currentPicker = ref<'start' | 'end' | null>(null)
const pickerH = ref(9)
const pickerM = ref(0)

const showStartPicker = computed(() => currentPicker.value === 'start')
const showEndPicker = computed(() => currentPicker.value === 'end')

function pad2(n: number) { return String(n).padStart(2, '0') }

function parseTime(val: string) {
  const m = (val || '').match(/^(\d{1,2}):(\d{2})$/)
  return m ? { h: parseInt(m[1]), m: parseInt(m[2]) } : null
}

function syncPickerValues() {
  const target = currentPicker.value === 'start' ? form.start_time : form.end_time
  const t = parseTime(target)
  pickerH.value = t ? t.h : 9
  pickerM.value = t ? t.m : 0
}

function openPicker(which: 'start' | 'end') {
  currentPicker.value = which
  syncPickerValues()
}

function closePicker() {
  currentPicker.value = null
}

function applyPreset(t: string) {
  if (currentPicker.value === 'start') form.start_time = t
  else if (currentPicker.value === 'end') form.end_time = t
  closePicker()
}

function confirmPicker() {
  const val = `${pad2(pickerH.value)}:${pad2(pickerM.value)}`
  if (currentPicker.value === 'start') form.start_time = val
  else if (currentPicker.value === 'end') form.end_time = val
  closePicker()
}

function adjustHour(delta: number) {
  pickerH.value = Math.max(0, Math.min(23, pickerH.value + delta))
}

function adjustMin(delta: number) {
  let m = pickerM.value + delta
  if (m >= 60) { m -= 60; pickerH.value = Math.min(23, pickerH.value + 1) }
  if (m < 0) { m += 60; pickerH.value = Math.max(0, pickerH.value - 1) }
  pickerM.value = Math.round(m / 5) * 5
  if (pickerM.value >= 60) pickerM.value = 55
}

const timePresets = ['06:00','07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00']

const quickTimes = [
  { label: '清晨 6:00', value: '06:00' },
  { label: '上午 9:00', value: '09:00' },
  { label: '中午 12:00', value: '12:00' },
  { label: '下午 3:00', value: '15:00' },
  { label: '傍晚 6:00', value: '18:00' },
  { label: '晚上 9:00', value: '21:00' },
]

// ESC 关闭
function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape' && currentPicker.value) closePicker()
}

onMounted(() => document.addEventListener('keydown', onKeydown))
onUnmounted(() => document.removeEventListener('keydown', onKeydown))

const alternatives = ref([
  { name: '替代景点 A', rating: 4.5, price: 120 },
  { name: '替代景点 B', rating: 4.2, price: 80 },
  { name: '替代景点 C', rating: 4.7, price: 150 },
])

watch(() => props.activity, (val) => {
  if (val) {
    Object.assign(form, JSON.parse(JSON.stringify(val)))
    isNew.value = false
  } else {
    Object.assign(form, {
      id: '', type: 'attraction', name: '', description: '', address: '',
      lat: 0, lng: 0, start_time: '09:00', end_time: '10:00',
      price: 0, tags: [], notes: '',
    })
    isNew.value = true
  }
}, { immediate: true })

function addTag() {
  const tag = tagInput.value.trim()
  if (tag && !form.tags.includes(tag)) form.tags.push(tag)
  tagInput.value = ''
}

function removeTag(tag: string) {
  form.tags = form.tags.filter(t => t !== tag)
}

function handleSave() {
  emit('save', { ...form, id: form.id || `act-${Date.now()}` })
  emit('update:visible', false)
}

function replace(alt: any) {
  if (props.activity) {
    emit('replace', props.activity, {
      ...props.activity,
      name: alt.name,
      price: alt.price,
    })
  }
}

function onMapSelect(lat: number, lng: number, address: string) {
  form.lat = lat
  form.lng = lng
  form.address = address
}
</script>

<style scoped lang="scss">
// ==========================================
// 全屏对话框 — 大地素雅风
// ==========================================

// ── 顶部栏 ──
.dialog-topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 48px;
  background: linear-gradient(180deg, var(--color-warm-white, #FAF8F3) 60%, rgba(250,248,243,0.92));
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(166, 139, 122, 0.1);
}

.topbar-left {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.topbar-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-primary, #3D3D3D);
  letter-spacing: 1px;
}

.topbar-subtitle {
  font-size: 13px;
  color: var(--color-text-secondary, #6B6B6B);
}

.topbar-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 1.5px solid transparent;
  border-radius: 50%;
  background: transparent;
  color: var(--color-text-secondary, #6B6B6B);
  cursor: pointer;
  opacity: 0.6;
  transition: all 0.25s ease;

  &:hover {
    opacity: 1;
    color: var(--color-warm-brown, #A68B7A);
    background: rgba(166, 139, 122, 0.08);
    border-color: rgba(166, 139, 122, 0.2);
    transform: rotate(90deg);
  }
}

// ── 内容区 ──
.dialog-body {
  flex: 1;
  overflow-y: auto;
  padding: 32px 48px 40px;
}

.form-container {
  max-width: 900px;
  margin: 0 auto;
}

// ── 分区卡片 ──
.section-card {
  background: var(--color-cream, #FDFBF7);
  border: 1.5px solid rgba(166, 139, 122, 0.08);
  border-radius: 16px;
  padding: 20px 24px;
  transition: border-color 0.2s;

  &:hover {
    border-color: rgba(166, 139, 122, 0.15);
  }
}

.section-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-warm-brown, #A68B7A);
  margin-bottom: 12px;
  letter-spacing: 0.4px;
  text-transform: uppercase;
  opacity: 0.85;
}

// ── 两列布局 ──
.form-two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

// ── 类型卡片 ──
.type-section {
  margin-bottom: 20px;
}

.type-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.type-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 10px 14px;
  background: var(--color-oat, #F5F0E8);
  border: 2px solid transparent;
  border-radius: 14px;
  color: var(--color-text-secondary, #6B6B6B);
  font-size: 13px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.25s ease;

  &:hover {
    background: #ebe4d9;
    border-color: rgba(166, 139, 122, 0.2);
  }

  &.active {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(166, 139, 122, 0.18);

    .tc-label { color: #fff; font-weight: 600; }

    .tc-img + .tc-label { color: #fff; }
  }

  &.card-attraction.active {
    background: linear-gradient(135deg, var(--color-sage, #B8C4B8), #9aad96);
    border-color: var(--color-sage, #B8C4B8);
  }
  &.card-restaurant.active {
    background: linear-gradient(135deg, var(--color-nude-pink, #E8D5D0), #d4bfb8);
    border-color: var(--color-nude-pink, #E8D5D0);
  }
  &.card-hotel.active {
    background: linear-gradient(135deg, var(--color-warm-brown, #A68B7A), #8f7362);
    border-color: var(--color-warm-brown, #A68B7A);
  }
  &.card-transport.active {
    background: linear-gradient(135deg, #c4bfb4, #a89f92);
    border-color: #c4bfb4;
  }
}

.tc-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: rgba(166, 139, 122, 0.1);
  transition: all 0.25s;

  .active & {
    background: rgba(255,255,255,0.28);
  }
}

.tc-img { width: 20px; height: 20px; border-radius: 4px; object-fit: cover; }
.tc-label { transition: color 0.25s; }

// ── 输入框 ──
.input-field {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.input-prefix-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-warm-brown, #A68B7A);
  opacity: 0.45;
  pointer-events: none;
  z-index: 1;
}

.native-input {
  width: 100%;
  height: 46px;
  padding: 0 16px 0 40px;
  background: var(--color-warm-white, #FAF8F3);
  border: 1.5px solid rgba(166, 139, 122, 0.15);
  border-radius: 12px;
  color: var(--color-text-primary, #3D3D3D);
  font-size: 15px;
  font-weight: 500;
  font-family: inherit;
  outline: none;
  box-sizing: border-box;
  transition: all 0.25s ease;

  &::placeholder { color: #c5c0b7; font-weight: 400; }

  &:hover {
    border-color: rgba(166, 139, 122, 0.35);
    background: #fff;
  }

  &:focus {
    border-color: var(--color-warm-brown, #A68B7A);
    background: #fff;
    box-shadow: 0 0 0 4px rgba(166, 139, 122, 0.07);
  }
}

// ── 高级时间选择器 ──
.time-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tu-icon {
  color: var(--color-warm-brown, #A68B7A);
  opacity: 0.45;
  flex-shrink: 0;
}

// ── Teleport 时间选择器：触发器按钮 ──
.time-trigger-btn {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  height: 46px;
  padding: 0 14px;
  background: var(--color-warm-white, #FAF8F3);
  border: 1.5px solid rgba(166, 139, 122, 0.15);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
  user-select: none;
  font-family: inherit;

  &:hover {
    border-color: rgba(166, 139, 122, 0.35);
    background: #fff;
    box-shadow: 0 2px 10px rgba(166, 139, 122, 0.06);
  }

  &.active {
    border-color: var(--color-warm-brown, #A68B7A);
    box-shadow: 0 0 0 4px rgba(166, 139, 122, 0.07), 0 4px 16px rgba(166, 139, 122, 0.1);
    background: #fff;
  }
}

.tu-text {
  flex: 1;
  font-size: 15px;
  font-weight: 700;
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  letter-spacing: 1px;
  color: var(--color-text-primary, #3D3D3D);

  &:empty::before {
    content: '--:--';
    color: #c5c0b7;
    font-weight: 400;
    font-family: inherit;
  }
}

.tu-chevron {
  color: var(--color-warm-brown, #A68B7A);
  opacity: 0.4;
  transition: transform 0.25s ease;
  flex-shrink: 0;

  .time-trigger-btn.active & {
    transform: rotate(180deg);
  }
}

// ── Teleport 居中浮层 ──
.time-overlay {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(61, 61, 61, 0.35);
  backdrop-filter: blur(4px);
}

.time-panel {
  width: 380px;
  max-width: 92vw;
  background: #fff;
  border: 1.5px solid rgba(166, 139, 122, 0.12);
  border-radius: 20px;
  box-shadow: 0 24px 64px rgba(61, 61, 61, 0.15), 0 4px 16px rgba(166, 139, 122, 0.08);
  overflow: hidden;
  animation: tpPanelIn 0.22s ease-out;
}

@keyframes tpPanelIn {
  from { opacity: 0; transform: translateY(12px) scale(0.96); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

.tp-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 22px 14px;
}

.tp-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text-primary, #3D3D3D);
  letter-spacing: 0.3px;
}

.tp-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border: 1.5px solid transparent;
  border-radius: 50%;
  background: transparent;
  color: var(--color-text-secondary, #6B6B6B);
  cursor: pointer;
  opacity: 0.5;
  transition: all 0.2s ease;

  &:hover {
    opacity: 1;
    color: var(--color-warm-brown, #A68B7A);
    background: rgba(166, 139, 122, 0.06);
    border-color: rgba(166, 139, 122, 0.15);
  }
}

// 预设时间网格
.tp-presets-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 6px;
  padding: 0 20px 16px;
}

.tp-preset-chip {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 38px;
  border: 1.5px solid transparent;
  border-radius: 10px;
  background: var(--color-oat, #F5F0E8);
  color: var(--color-text-secondary, #6B6B6B);
  font-size: 12px;
  font-weight: 600;
  font-family: 'SF Mono', monospace;
  cursor: pointer;
  transition: all 0.15s ease;
  letter-spacing: 0.3px;

  &:hover {
    background: #ebe4d9;
    border-color: rgba(166, 139, 122, 0.2);
    color: var(--color-warm-brown, #A68B7A);
  }

  &.active {
    background: linear-gradient(135deg, var(--color-sage, #B8C4B8), #9aad96);
    border-color: var(--color-sage, #B8C4B8);
    color: #fff;
    box-shadow: 0 2px 8px rgba(184, 196, 184, 0.3);
  }
}

// 分隔线
.tp-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 20px 14px;

  &::before,
  &::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(166, 139, 122, 0.12);
  }

  span {
    font-size: 12px;
    font-weight: 500;
    color: var(--color-warm-brown, #A68B7A);
    opacity: 0.6;
    letter-spacing: 0.4px;
    white-space: nowrap;
  }
}

// 自定义时分滚动器
.tp-custom {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 0 20px 14px;
}

.tp-custom-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.tp-custom-label {
  font-size: 11px;
  font-weight: 500;
  color: var(--color-warm-brown, #A68B7A);
  opacity: 0.5;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tp-spin {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: var(--color-warm-white, #FAF8F3);
  border: 1.5px solid rgba(166, 139, 122, 0.12);
  border-radius: 12px;
  padding: 4px 10px;
  gap: 2px;
}

.tp-spin-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 24px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--color-warm-brown, #A68B7A);
  cursor: pointer;
  opacity: 0.5;
  transition: all 0.15s;

  &:hover {
    opacity: 1;
    background: rgba(166, 139, 122, 0.08);
    transform: translateY(-1px);
  }

  &:last-child:hover {
    transform: translateY(1px);
  }
}

.tp-spin-val {
  font-size: 28px;
  font-weight: 700;
  font-family: 'SF Mono', 'Cascadia Code', monospace;
  color: var(--color-text-primary, #3D3D3D);
  line-height: 1.2;
  letter-spacing: 1px;
  user-select: none;
  min-width: 48px;
  text-align: center;
}

.tp-custom-sep {
  font-size: 26px;
  font-weight: 300;
  color: var(--color-warm-brown, #A68B7A);
  opacity: 0.35;
  line-height: 1;
  padding-bottom: 20px;
}

// 快捷按钮行
.tp-quick-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  padding: 0 20px 14px;
}

.tp-quick-btn {
  padding: 6px 16px;
  border: 1.5px solid rgba(166, 139, 122, 0.12);
  border-radius: 20px;
  background: var(--color-warm-white, #FAF8F3);
  color: var(--color-warm-brown, #A68B7A);
  font-size: 12px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(166, 139, 122, 0.08);
    border-color: rgba(166, 139, 122, 0.28);
    transform: translateY(-1px);
  }
}

// 确定按钮
.tp-confirm {
  width: calc(100% - 40px);
  margin: 0 20px 20px;
  padding: 13px 0;
  background: linear-gradient(135deg, var(--color-warm-brown, #A68B7A), #8f7362);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  font-family: inherit;
  letter-spacing: 0.5px;
  cursor: pointer;
  box-shadow: 0 3px 16px rgba(166, 139, 122, 0.28);
  transition: all 0.25s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 24px rgba(166, 139, 122, 0.38);
    background: linear-gradient(135deg, #b59a88, var(--color-warm-brown, #A68B7A));
  }

  &:active { transform: translateY(0); }
}

// ── Transition 动画 ──
.tp-overlay-enter-active {
  transition: opacity 0.2s ease;

  .time-panel {
    animation: tpPanelIn 0.22s ease-out;
  }
}

.tp-overlay-leave-active {
  transition: opacity 0.16s ease;

  .time-panel {
    animation: tpPanelOut 0.16s ease-in forwards;
  }
}

.tp-overlay-enter-from,
.tp-overlay-leave-to { opacity: 0; }

@keyframes tpPanelOut {
  from { opacity: 1; transform: translateY(0) scale(1); }
  to   { opacity: 0; transform: translateY(-8px) scale(0.96); }
}

.time-arrow {
  color: var(--color-warm-brown, #A68B7A);
  opacity: 0.4;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  padding: 0 2px;
}

// ── 地图按钮 ──
.map-fab {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1.5px solid rgba(166, 139, 122, 0.2);
  border-radius: 10px;
  background: var(--color-oat, #F5F0E8);
  color: var(--color-warm-brown, #A68B7A);
  cursor: pointer;
  flex-shrink: 0;
  margin-right: -4px;
  transition: all 0.25s ease;

  &:hover {
    background: var(--color-sage, #B8C4B8);
    border-color: var(--color-sage, #B8C4B8);
    color: #fff;
    transform: scale(1.06);
  }
}

// ── 价格 ──
.price-field {
  display: flex;
  align-items: center;
  background: var(--color-warm-white, #FAF8F3);
  border: 1.5px solid rgba(166, 139, 122, 0.15);
  border-radius: 12px;
  height: 46px;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
  transition: all 0.25s ease;

  &:hover {
    border-color: rgba(166, 139, 122, 0.35);
    background: #fff;
  }

  &:focus-within {
    border-color: var(--color-warm-brown, #A68B7A);
    box-shadow: 0 0 0 4px rgba(166, 139, 122, 0.07);
    background: #fff;
  }
}

.price-prepend {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 100%;
  color: var(--color-warm-brown, #A68B7A);
  font-size: 16px;
  font-weight: 700;
  background: rgba(166, 139, 122, 0.06);
  border-right: 1.5px solid rgba(166, 139, 122, 0.08);
  flex-shrink: 0;
}

.price-num {
  flex: 1;
  height: 100%;
  padding: 0 12px;
  background: transparent;
  border: none;
  outline: none;
  color: var(--color-text-primary, #3D3D3D);
  font-size: 15px;
  font-weight: 600;
  font-family: inherit;
  -moz-appearance: textfield;

  &::-webkit-outer-spin-button,
  &::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }

  &::placeholder { color: #c5c0b7; font-weight: 400; }
}

.price-steppers {
  display: flex;
  height: 100%;
  border-left: 1.5px solid rgba(166, 139, 122, 0.08);
}

.step-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 100%;
  border: none;
  background: transparent;
  color: var(--color-warm-brown, #A68B7A);
  opacity: 0.55;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(166, 139, 122, 0.06);
    opacity: 1;
  }

  &.plus {
    border-left: 1.5px solid rgba(166, 139, 122, 0.08);
  }
}

// ── 标签 ──
.tags-box {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: var(--color-warm-white, #FAF8F3);
  border: 1.5px solid rgba(166, 139, 122, 0.15);
  border-radius: 12px;
  min-height: 48px;
  width: 100%;
  box-sizing: border-box;
  transition: all 0.25s ease;

  &:focus-within {
    border-color: var(--color-warm-brown, #A68B7A);
    box-shadow: 0 0 0 4px rgba(166, 139, 122, 0.07);
  }
}

.tag-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 11px;
  background: linear-gradient(135deg, rgba(184, 196, 184, 0.3), rgba(166, 139, 122, 0.12));
  border: 1px solid rgba(184, 196, 184, 0.35);
  border-radius: 20px;
  color: var(--color-warm-brown, #A68B7A);
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.tag-x {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border: none;
  border-radius: 50%;
  background: rgba(166, 139, 122, 0.15);
  color: var(--color-warm-brown, #A68B7A);
  font-size: 14px;
  line-height: 1;
  cursor: pointer;
  font-family: inherit;
  padding: 0;
  opacity: 0.6;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(180, 120, 110, 0.2);
    opacity: 1;
    transform: scale(1.1);
  }
}

.tag-new-input {
  flex: 1;
  min-width: 80px;
  border: none;
  outline: none;
  background: transparent;
  color: var(--color-text-primary, #3D3D3D);
  font-size: 13px;
  font-family: inherit;
  padding: 4px 0;

  &::placeholder { color: #c5c0b7; }
}

// ── 备注 ──
.native-textarea {
  width: 100%;
  padding: 12px 16px;
  background: var(--color-warm-white, #FAF8F3);
  border: 1.5px solid rgba(166, 139, 122, 0.15);
  border-radius: 12px;
  color: var(--color-text-primary, #3D3D3D);
  font-size: 14px;
  font-family: inherit;
  outline: none;
  resize: vertical;
  box-sizing: border-box;
  transition: all 0.25s ease;

  &::placeholder { color: #c5c0b7; }

  &:hover {
    border-color: rgba(166, 139, 122, 0.35);
    background: #fff;
  }

  &:focus {
    border-color: var(--color-warm-brown, #A68B7A);
    box-shadow: 0 0 0 4px rgba(166, 139, 122, 0.07);
    background: #fff;
  }
}

// ── AI 区域 ──
.ai-section {
  margin-top: 20px;
}

.ai-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 14px 20px;
  background: linear-gradient(135deg, rgba(166, 139, 122, 0.04), rgba(232, 213, 208, 0.08));
  border: 1.5px solid rgba(166, 139, 122, 0.14);
  border-radius: 14px;
  color: var(--color-warm-brown, #A68B7A);
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.25s ease;

  &:hover {
    background: linear-gradient(135deg, rgba(166, 139, 122, 0.08), rgba(232, 213, 208, 0.12));
    border-color: rgba(166, 139, 122, 0.24);
  }
}

.ai-toggle-left {
  display: flex;
  align-items: center;
  gap: 10px;

  svg { opacity: 0.7; }
}

.ai-chevron {
  transition: transform 0.3s ease;
  color: var(--color-warm-brown, #A68B7A);
  opacity: 0.5;

  &.flipped { transform: rotate(180deg); }
}

.ai-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 14px;
}

.ai-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  background: var(--color-warm-white, #FAF8F3);
  border: 1.5px solid rgba(166, 139, 122, 0.08);
  border-radius: 14px;
  transition: all 0.2s ease;

  &:hover {
    border-color: rgba(166, 139, 122, 0.22);
    box-shadow: 0 2px 10px rgba(166, 139, 122, 0.06);
    transform: translateY(-1px);
  }
}

.ai-item-info { flex: 1; min-width: 0; }
.ai-item-name { font-size: 14px; font-weight: 600; color: var(--color-text-primary, #3D3D3D); }
.ai-item-meta { display: flex; align-items: center; gap: 12px; margin-top: 4px; }
.ai-item-stars { font-size: 12px; color: var(--color-warm-brown, #A68B7A); font-weight: 500; }
.ai-item-price { font-size: 13px; font-weight: 700; color: var(--color-nude-pink, #E8D5D0); }

.ai-replace-btn {
  padding: 7px 20px;
  border: 1.5px solid var(--color-warm-brown, #A68B7A);
  border-radius: 10px;
  background: transparent;
  color: var(--color-warm-brown, #A68B7A);
  font-size: 13px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.25s ease;

  &:hover {
    background: var(--color-warm-brown, #A68B7A);
    color: #fff;
    transform: translateY(-1px);
    box-shadow: 0 3px 12px rgba(166, 139, 122, 0.22);
  }
}

// ── 底部栏 ──
.dialog-bottombar {
  position: sticky;
  bottom: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 14px;
  padding: 16px 48px;
  background: linear-gradient(0deg, var(--color-warm-white, #FAF8F3) 60%, rgba(250,248,243,0.92));
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(166, 139, 122, 0.1);
}

.btn-cancel {
  height: 44px;
  padding: 0 32px;
  background: transparent;
  border: 1.5px solid rgba(166, 139, 122, 0.25);
  border-radius: 12px;
  color: var(--color-text-secondary, #6B6B6B);
  font-size: 14px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.25s ease;

  &:hover {
    background: var(--color-oat, #F5F0E8);
    border-color: rgba(166, 139, 122, 0.4);
    color: var(--color-warm-brown, #A68B7A);
  }
}

.btn-confirm {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 44px;
  padding: 0 36px;
  background: linear-gradient(135deg, var(--color-warm-brown, #A68B7A), #8f7362);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  font-family: inherit;
  letter-spacing: 0.5px;
  cursor: pointer;
  box-shadow: 0 3px 16px rgba(166, 139, 122, 0.28);
  transition: all 0.25s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 24px rgba(166, 139, 122, 0.38);
    background: linear-gradient(135deg, #b59a88, var(--color-warm-brown, #A68B7A));
  }

  &:active {
    transform: translateY(0);
  }
}
</style>

<!-- el-dialog 全局样式覆盖 -->
<style lang="scss">
.activity-dialog {
  .el-dialog {
    width: 100% !important;
    height: 100% !important;
    margin: 0 !important;
    border-radius: 0 !important;
    background: var(--color-warm-white, #FAF8F3) !important;
    display: flex !important;
    flex-direction: column !important;
    padding: 0 !important;
    top: 0 !important;
    left: 0 !important;
  }

  .el-dialog__header {
    display: none !important;
  }

  .el-dialog__body {
    flex: 1 !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: column !important;
    padding: 0 !important;
  }

  .el-dialog__headerbtn {
    display: none !important;
  }

  .el-overlay {
    background: rgba(61, 61, 61, 0.35) !important;
  }
}
</style>
