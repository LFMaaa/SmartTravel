<template>
  <div class="poi-card" @click="$emit('click')">
    <div class="poi-cover" :style="{ background: coverGradient }">
      <div class="poi-cover-pattern"></div>
      <img class="poi-image" :src="coverImage" :alt="typeLabel" loading="lazy" />
      <div class="poi-badge-row">
        <span class="poi-badge">{{ typeLabel }}</span>
        <span v-if="poi.distance" class="poi-distance">{{ poi.distance }}</span>
      </div>
    </div>
    <div class="poi-body">
      <div class="poi-header">
        <h4 class="poi-name">{{ poi.name }}</h4>
        <div class="poi-rating" v-if="poi.rating">
          <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
          <span>{{ poi.rating.toFixed(1) }}</span>
        </div>
      </div>
      <div class="poi-meta">
        <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
        <span class="poi-city">{{ poi.city }}</span>
        <span class="poi-price" :class="{ free: !poi.price }">{{ poi.price > 0 ? `¥${poi.price}起` : '免费' }}</span>
      </div>
      <div class="poi-tags" v-if="poi.tags?.length">
        <span v-for="tag in poi.tags" :key="tag" class="poi-tag">{{ tag }}</span>
      </div>
      <p class="poi-desc" v-if="poi.description">{{ poi.description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { POIResult } from '@/types/search'
const props = defineProps<{ poi: POIResult }>()
defineEmits<{ click: [] }>()
const typeMap: Record<string, { label: string; emoji: string; gradient: string; image: string }> = {
  attraction: { label: '景点', emoji: '🏛️', gradient: 'linear-gradient(135deg, #0D7377, #14A3A8)', image: '/assets/poi/type_attraction.png' },
  hotel: { label: '酒店', emoji: '🏨', gradient: 'linear-gradient(135deg, #FF6B35, #E55A2B)', image: '/assets/poi/type_hotel.png' },
  restaurant: { label: '餐厅', emoji: '🍽️', gradient: 'linear-gradient(135deg, #F7A800, #FFC940)', image: '/assets/poi/type_restaurant.png' },
}
const typeLabel = computed(() => typeMap[props.poi.type]?.label || props.poi.type)
const coverEmoji = computed(() => typeMap[props.poi.type]?.emoji || '📍')
const coverGradient = computed(() => typeMap[props.poi.type]?.gradient || 'linear-gradient(135deg, #3b82f6, #8b5cf6)')
const coverImage = computed(() => typeMap[props.poi.type]?.image || '/assets/poi/type_attraction.png')
</script>

<style scoped lang="scss">
$bg-oat: #F5F0E8;
$brand-brown: #A68B7A;
$brand-sage: #B8C4B8;
$text-primary: #3D3D3D;
$text-secondary: #6B6B6B;
$text-muted: #B8B0A8;
$border: #E8D5D0;

.poi-card {
  background: $bg-oat; border-radius: 16px;
  border: 1px solid $border; overflow: hidden; cursor: pointer;
  transition: all 0.3s ease;
  &:hover {
    transform: translateY(-4px);
    border-color: rgba(245,158,11,0.2);
    box-shadow: 0 12px 28px rgba(0,0,0,0.4);
    .poi-image { transform: scale(1.08); }
  }
}

.poi-cover {
  height: 120px; display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden;
}

.poi-cover-pattern {
  position: absolute; inset: 0; opacity: 0.12;
  background-image:
    radial-gradient(circle at 20% 80%, rgba(255,255,255,0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255,255,255,0.08) 0%, transparent 40%),
    radial-gradient(circle at 50% 50%, rgba(255,255,255,0.06) 0%, transparent 70%);
}

.poi-image {
  width: 100%; height: 100%; object-fit: cover;
  position: relative; z-index: 1;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.poi-badge-row {
  position: absolute; top: 10px; left: 10px; right: 10px;
  display: flex; justify-content: space-between;
}

.poi-badge {
  padding: 3px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 600; color: #fff;
  background: rgba(0,0,0,0.35); backdrop-filter: blur(4px);
}

.poi-distance {
  padding: 3px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 500; color: #fff;
  background: rgba(0,0,0,0.25); backdrop-filter: blur(4px);
}

.poi-body { padding: 16px; }

.poi-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  gap: 10px; margin-bottom: 8px;
}

.poi-name { font-size: 15px; font-weight: 600; color: $text-primary; margin: 0; flex: 1; }

.poi-rating {
  display: flex; align-items: center; gap: 3px;
  color: $brand-brown; font-size: 13px; font-weight: 700; white-space: nowrap;
}

.poi-meta {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; color: $text-muted; margin-bottom: 10px;
  svg { flex-shrink: 0; }
}

.poi-city { flex: 1; }

.poi-price { font-weight: 600; color: $brand-brown; &.free { color: #10b981; } }

.poi-tags { display: flex; gap: 4px; flex-wrap: wrap; margin-bottom: 10px; }

.poi-tag {
  padding: 3px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 500;
  background: rgba(245,158,11,0.08); color: $brand-brown;
  border: 1px solid rgba(245,158,11,0.12);
}

.poi-desc {
  font-size: 12px; color: $text-muted; line-height: 1.5;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
</style>
