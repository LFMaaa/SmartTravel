<template>
  <el-drawer
    :model-value="visible"
    direction="rtl"
    size="520px"
    :title="isNew ? '添加活动' : '编辑活动'"
    class="activity-drawer"
    @update:model-value="$emit('update:visible', $event)"
  >
    <div class="drawer-root">
      <!-- 类型 Banner -->
      <div class="type-banner">
        <div class="banner-icon" :class="`icon-${form.type}`">
          <svg v-if="form.type === 'attraction'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="24" height="24"><path d="M3 21h18"/><path d="M5 21V7l8-4v18"/><path d="M19 21V11l-6-4"/></svg>
          <svg v-else-if="form.type === 'restaurant'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="24" height="24"><path d="M18 8h1a4 4 0 010 8h-1"/><path d="M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8z"/></svg>
          <svg v-else-if="form.type === 'hotel'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="24" height="24"><path d="M3 21h18"/><path d="M3 7v14h18V7l-3-4H6l-3 4z"/></svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="24" height="24"><rect x="1" y="3" width="15" height="13" rx="2"/><polygon points="16 8 20 8 23 11 23 16 16 16"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/></svg>
        </div>
        <div class="banner-text">
          <span class="banner-label">{{ typeLabel(form.type) }}</span>
          <span class="banner-hint">填写活动详情</span>
        </div>
      </div>

      <!-- 活动名称 -->
      <div class="form-group">
        <label class="form-label">活动名称</label>
        <div class="input-field">
          <svg class="input-prefix-icon" viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/></svg>
          <input
            v-model="form.name"
            placeholder="请输入活动名称"
            class="native-input"
            type="text"
          />
        </div>
      </div>

      <!-- 类型选择 -->
      <div class="form-group">
        <label class="form-label">类型</label>
        <div class="type-options">
          <button
            v-for="opt in typeOptions" :key="opt.value"
            class="type-opt"
            :class="{ on: form.type === opt.value }"
            @click="form.type = opt.value"
          >
            <img v-if="opt.value !== 'transport'" :src="`/assets/poi/type_${opt.value}.png`" class="type-opt-img" />
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" class="type-opt-svg"><rect x="1" y="3" width="15" height="13" rx="2"/><polygon points="16 8 20 8 23 11 23 16 16 16"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/></svg>
            <span>{{ opt.label }}</span>
          </button>
        </div>
      </div>

      <!-- 时间段 -->
      <div class="form-group">
        <label class="form-label">时间段</label>
        <div class="time-row">
          <div class="time-unit">
            <svg class="tu-icon" viewBox="0 0 18 18" fill="currentColor" width="14" height="14"><path fill-rule="evenodd" d="M9 16.5a7.5 7.5 0 100-15 7.5 7.5 0 000 15zm.75-9a.75.75 0 10-1.5 0v3c0 .2.08.39.22.53l2.12 2.12a.75.75 0 001.06-1.06L9.75 10.2V7.5z" clip-rule="evenodd"/></svg>
            <input v-model="form.start_time" placeholder="09:00" class="time-num" type="text" maxlength="5" />
          </div>
          <span class="time-arrow">→</span>
          <div class="time-unit">
            <svg class="tu-icon" viewBox="0 0 18 18" fill="currentColor" width="14" height="14"><path fill-rule="evenodd" d="M9 16.5a7.5 7.5 0 100-15 7.5 7.5 0 000 15zm.75-9a.75.75 0 10-1.5 0v3c0 .2.08.39.22.53l2.12 2.12a.75.75 0 001.06-1.06L9.75 10.2V7.5z" clip-rule="evenodd"/></svg>
            <input v-model="form.end_time" placeholder="10:00" class="time-num" type="text" maxlength="5" />
          </div>
        </div>
      </div>

      <!-- 地址 -->
      <div class="form-group">
        <label class="form-label">地址</label>
        <div class="input-field">
          <svg class="input-prefix-icon" viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
          <input
            v-model="form.address"
            placeholder="请输入活动地址"
            class="native-input"
            type="text"
          />
          <button class="map-fab" @click="showMap = true" title="地图选点">
            <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
          </button>
        </div>
      </div>

      <!-- 预算费用 -->
      <div class="form-group">
        <label class="form-label">预算费用 （元）</label>
        <div class="price-field">
          <div class="price-prepend">¥</div>
          <input
            v-model.number="form.price"
            type="number"
            min="0"
            step="50"
            class="price-num"
            placeholder="0"
          />
          <div class="price-steppers">
            <button class="step-btn" @click="form.price = Math.max(0, (form.price||0) - 50)">−</button>
            <button class="step-btn plus" @click="form.price = (form.price||0) + 50">+</button>
          </div>
        </div>
      </div>

      <!-- 标签 -->
      <div class="form-group">
        <label class="form-label">标签</label>
        <div class="tags-box">
          <span v-for="tag in form.tags" :key="tag" class="tag-badge">
            {{ tag }}
            <button class="tag-x" @click="removeTag(tag)">&#x00d7;</button>
          </span>
          <input
            v-model="tagInput"
            placeholder="输入标签后按回车"
            class="tag-new-input"
            @keyup.enter="addTag"
          />
        </div>
      </div>

      <!-- 备注 -->
      <div class="form-group">
        <label class="form-label">备注</label>
        <textarea
          v-model="form.notes"
          placeholder="备注信息（可选）"
          class="native-textarea"
          rows="3"
        ></textarea>
      </div>

      <!-- AI 推荐备选 -->
      <div v-if="!isNew" class="ai-section">
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
                <span class="ai-item-stars">★ {{ alt.rating }}</span>
                <span class="ai-item-price">¥{{ alt.price }}</span>
              </div>
            </div>
            <button class="ai-replace-btn" @click="replace(alt)">替换</button>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="footer-row">
        <button class="btn-cancel" @click="$emit('update:visible', false)">取消</button>
        <button class="btn-confirm" @click="handleSave">
          <svg viewBox="0 0 20 20" fill="currentColor" width="15" height="15"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
          保存活动
        </button>
      </div>
    </template>

    <MapPopup v-if="showMap" :lat="form.lat" :lng="form.lng" :name="form.name" @close="showMap = false" />
  </el-drawer>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
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
</script>

<style scoped lang="scss">
// ==========================================
// Root — 无依赖原生控件，暗色主题写死
// ==========================================
.drawer-root {
  padding: 0 0 16px;
  width: 100%;
  box-sizing: border-box;
}

// ==========================================
// Type Banner
// ==========================================
.type-banner {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 20px;
  margin-bottom: 24px;
  background: linear-gradient(135deg, rgba(245,158,11,0.07), rgba(59,130,246,0.05));
  border-radius: 16px;
  border: 1px solid rgba(245,158,11,0.12);
  width: 100%;
  box-sizing: border-box;
}

.banner-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 14px;
  flex-shrink: 0;
  color: #fff;
  &.icon-attraction { background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
  &.icon-restaurant { background: linear-gradient(135deg, #f59e0b, #d97706); }
  &.icon-hotel     { background: linear-gradient(135deg, #8b5cf6, #6d28d9); }
  &.icon-transport { background: linear-gradient(135deg, #10b981, #047857); }
}

.banner-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.banner-label { font-size: 16px; font-weight: 700; color: #f1f5f9; }
.banner-hint  { font-size: 12px; color: #64748b; }

// ==========================================
// Form Group
// ==========================================
.form-group {
  margin-bottom: 20px;
  width: 100%;
  box-sizing: border-box;
}
.form-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 8px;
}

// ==========================================
// Native Input
// ==========================================
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
  color: #64748b;
  pointer-events: none;
  z-index: 1;
}

.native-input {
  width: 100%;
  height: 44px;
  padding: 0 16px 0 40px;
  background: #1a2235;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  color: #f1f5f9;
  font-size: 14px;
  font-weight: 500;
  font-family: inherit;
  outline: none;
  box-sizing: border-box;
  transition: all 0.2s ease;

  &::placeholder { color: #64748b; }

  &:hover {
    border-color: rgba(245,158,11,0.35);
    background: #1e293b;
  }

  &:focus {
    border-color: rgba(245,158,11,0.5);
    background: #1a2235;
    box-shadow: 0 0 0 3px rgba(245,158,11,0.1);
  }
}

// ==========================================
// Type options
// ==========================================
.type-options {
  display: flex;
  gap: 8px;
  width: 100%;
}
.type-opt {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 11px 6px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  color: #94a3b8;
  font-size: 13px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(255,255,255,0.06);
    border-color: rgba(255,255,255,0.14);
    color: #cbd5e1;
  }

  &.on {
    background: rgba(245,158,11,0.12);
    border-color: rgba(245,158,11,0.4);
    color: #f59e0b;
    box-shadow: 0 0 12px rgba(245,158,11,0.12);
  }
}
.type-opt-img { width: 20px; height: 20px; border-radius: 5px; object-fit: cover; flex-shrink: 0; }
.type-opt-svg { width: 20px; height: 20px; flex-shrink: 0; }

// ==========================================
// Time picker
// ==========================================
.time-row {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}
.time-unit {
  flex: 1;
  display: flex;
  align-items: center;
  background: #1a2235;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  padding: 0 14px;
  height: 44px;
  gap: 10px;
  transition: all 0.2s ease;

  &:hover {
    border-color: rgba(245,158,11,0.35);
    background: #1e293b;
  }

  &:focus-within {
    border-color: rgba(245,158,11,0.5);
    box-shadow: 0 0 0 3px rgba(245,158,11,0.1);
  }
}
.tu-icon {
  color: #64748b;
  flex-shrink: 0;
}
.time-num {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #f1f5f9;
  font-size: 15px;
  font-weight: 600;
  font-family: inherit;
  &::placeholder { color: #64748b; font-weight: 400; }
}
.time-arrow {
  color: #64748b;
  font-size: 15px;
  font-weight: 600;
  flex-shrink: 0;
  padding: 0 4px;
}

// ==========================================
// Map button (in address field)
// ==========================================
.map-fab {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 8px;
  background: rgba(59,130,246,0.12);
  color: #60a5fa;
  cursor: pointer;
  flex-shrink: 0;
  margin-right: -4px;
  transition: all 0.2s;

  &:hover {
    background: rgba(59,130,246,0.22);
    color: #93c5fd;
  }
}

// ==========================================
// Price
// ==========================================
.price-field {
  display: flex;
  align-items: center;
  background: #1a2235;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  height: 44px;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
  transition: all 0.2s ease;

  &:hover {
    border-color: rgba(245,158,11,0.35);
    background: #1e293b;
  }

  &:focus-within {
    border-color: rgba(245,158,11,0.5);
    box-shadow: 0 0 0 3px rgba(245,158,11,0.1);
    background: #1a2235;
  }
}

.price-prepend {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 100%;
  color: #f59e0b;
  font-size: 16px;
  font-weight: 700;
  background: rgba(245,158,11,0.06);
  border-right: 1px solid rgba(255,255,255,0.08);
  flex-shrink: 0;
}

.price-num {
  flex: 1;
  height: 100%;
  padding: 0 12px;
  background: transparent;
  border: none;
  outline: none;
  color: #f1f5f9;
  font-size: 15px;
  font-weight: 600;
  font-family: inherit;
  -moz-appearance: textfield;
  &::-webkit-outer-spin-button,
  &::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
  &::placeholder { color: #64748b; font-weight: 400; }
}

.price-steppers {
  display: flex;
  height: 100%;
  border-left: 1px solid rgba(255,255,255,0.08);
}

.step-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 100%;
  border: none;
  background: transparent;
  color: #94a3b8;
  font-size: 16px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s;

  &:hover {
    background: rgba(245,158,11,0.12);
    color: #f59e0b;
  }

  &.plus {
    border-left: 1px solid rgba(255,255,255,0.08);
  }
}

// ==========================================
// Tags
// ==========================================
.tags-box {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: #1a2235;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  min-height: 48px;
  width: 100%;
  box-sizing: border-box;
  transition: all 0.2s ease;

  &:focus-within {
    border-color: rgba(245,158,11,0.5);
    box-shadow: 0 0 0 3px rgba(245,158,11,0.1);
  }
}

.tag-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  background: rgba(59,130,246,0.1);
  border: 1px solid rgba(59,130,246,0.18);
  border-radius: 20px;
  color: #93c5fd;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.tag-x {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border: none;
  border-radius: 50%;
  background: rgba(59,130,246,0.18);
  color: #93c5fd;
  font-size: 14px;
  line-height: 1;
  cursor: pointer;
  font-family: inherit;
  padding: 0;

  &:hover { background: rgba(239,68,68,0.3); color: #fca5a5; }
}

.tag-new-input {
  flex: 1;
  min-width: 80px;
  border: none;
  outline: none;
  background: transparent;
  color: #f1f5f9;
  font-size: 13px;
  font-family: inherit;
  padding: 4px 0;

  &::placeholder { color: #64748b; }
}

// ==========================================
// Textarea
// ==========================================
.native-textarea {
  width: 100%;
  padding: 12px 16px;
  background: #1a2235;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  color: #f1f5f9;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  resize: vertical;
  box-sizing: border-box;
  transition: all 0.2s ease;

  &::placeholder { color: #64748b; }

  &:hover {
    border-color: rgba(245,158,11,0.35);
    background: #1e293b;
  }

  &:focus {
    border-color: rgba(245,158,11,0.5);
    box-shadow: 0 0 0 3px rgba(245,158,11,0.1);
    background: #1a2235;
  }
}

// ==========================================
// AI replacements
// ==========================================
.ai-section {
  margin-top: 4px;
  width: 100%;
}
.ai-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 12px 16px;
  background: rgba(245,158,11,0.06);
  border: 1px solid rgba(245,158,11,0.14);
  border-radius: 10px;
  color: #f59e0b;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: rgba(245,158,11,0.1);
    border-color: rgba(245,158,11,0.24);
  }
}
.ai-toggle-left {
  display: flex;
  align-items: center;
  gap: 8px;
}
.ai-chevron {
  transition: transform 0.25s ease;
  color: #f59e0b;
  &.flipped { transform: rotate(180deg); }
}
.ai-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 10px;
}
.ai-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 10px;
  transition: border-color 0.2s;

  &:hover { border-color: rgba(255,255,255,0.12); }
}
.ai-item-info { flex: 1; min-width: 0; }
.ai-item-name { font-size: 14px; font-weight: 600; color: #e2e8f0; }
.ai-item-meta { display: flex; align-items: center; gap: 12px; margin-top: 4px; }
.ai-item-stars { font-size: 12px; color: #f59e0b; font-weight: 500; }
.ai-item-price { font-size: 13px; font-weight: 700; color: #f59e0b; }
.ai-replace-btn {
  padding: 6px 16px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #0f172a;
  font-size: 13px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.2s;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(245,158,11,0.3);
  }
}

// ==========================================
// Footer
// ==========================================
.footer-row {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  width: 100%;
}

.btn-cancel {
  height: 42px;
  padding: 0 24px;
  background: transparent;
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 10px;
  color: #94a3b8;
  font-size: 14px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: rgba(255,255,255,0.05);
    border-color: rgba(255,255,255,0.2);
    color: #e2e8f0;
  }
}

.btn-confirm {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 42px;
  padding: 0 28px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border: none;
  border-radius: 10px;
  color: #0f172a;
  font-size: 14px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(245,158,11,0.3);
  transition: all 0.2s;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 22px rgba(245,158,11,0.4);
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
  }
}
</style>

<!-- el-drawer 外壳暗色（不影响原生控件） -->
<style lang="scss">
.activity-drawer {
  background: #111827 !important;

  .el-drawer__header { color: #f1f5f9 !important; border-bottom: 1px solid rgba(255,255,255,0.06) !important; }
  .el-drawer__body   { background: #111827 !important; }
  .el-drawer__footer { border-top: 1px solid rgba(255,255,255,0.06) !important; background: #111827 !important; }

  .el-drawer__close-btn {
    width: 30px !important; height: 30px !important; border-radius: 8px; color: #64748b !important;
    svg { width: 18px !important; height: 18px !important; }
    &:hover { color: #f1f5f9 !important; background: rgba(255,255,255,0.06); }
  }
}
</style>
