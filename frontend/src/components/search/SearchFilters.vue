<template>
  <div class="search-filters">
    <div class="filter-group">
      <span class="filter-label">城市</span>
      <div class="filter-chips">
        <button v-for="city in cities" :key="city" :class="['filter-chip', { active: localFilters.city === city }]" @click="toggleFilter('city', city)">{{ city }}</button>
      </div>
    </div>
    <div class="filter-divider"></div>
    <div class="filter-group">
      <span class="filter-label">类型</span>
      <div class="filter-chips">
        <button v-for="pt in poiTypes" :key="pt.value" :class="['filter-chip', { active: localFilters.poi_type === pt.value }]" @click="toggleFilter('poi_type', pt.value)">
          <img class="chip-icon" :src="pt.image" :alt="pt.label" />
          {{ pt.label }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ modelValue: Record<string, string> }>()
const emit = defineEmits<{ 'update:modelValue': [Record<string, string>] }>()
const cities = ['北京', '成都', '上海', '西安', '三亚', '云南']
const poiTypes = [
  { value: 'attraction', label: '景点', emoji: '🏛️', image: '/assets/poi/type_attraction.png' },
  { value: 'hotel', label: '酒店', emoji: '🏨', image: '/assets/poi/type_hotel.png' },
  { value: 'restaurant', label: '餐厅', emoji: '🍽️', image: '/assets/poi/type_restaurant.png' },
]
const localFilters = computed({ get: () => props.modelValue, set: (val) => emit('update:modelValue', val) })
function toggleFilter(key: string, value: string) {
  const current = { ...localFilters.value }
  current[key] = current[key] === value ? '' : value
  emit('update:modelValue', current)
}
</script>

<style scoped lang="scss">
$bg-elevated: #1a2235;
$brand-amber: #f59e0b;
$text-secondary: #94a3b8;
$text-muted: #64748b;
$border: #1e293b;

.search-filters {
  display: flex; align-items: center; gap: 20px;
  margin-top: 16px; max-width: 640px; margin-left: auto; margin-right: auto;
  padding: 12px 20px;
  background: $bg-elevated; border-radius: 14px;
  border: 1px solid $border;
  flex-wrap: wrap; justify-content: center;
}

.filter-group { display: flex; align-items: center; gap: 8px; }

.filter-label {
  font-size: 12px; font-weight: 600; color: $text-muted;
  text-transform: uppercase; letter-spacing: 1px;
}

.filter-chips { display: flex; gap: 6px; flex-wrap: wrap; }

.filter-chip {
  display: flex; align-items: center; gap: 4px;
  padding: 6px 14px;
  background: transparent; border: 1px solid $border;
  border-radius: 20px; font-size: 12px; color: $text-secondary;
  cursor: pointer; font-family: inherit;
  transition: all 0.25s ease;
  &:hover { border-color: $brand-amber; color: $brand-amber; }
  &.active { background: rgba(245,158,11,0.08); border-color: $brand-amber; color: $brand-amber; font-weight: 600; }
}

.chip-icon { width: 18px; height: 18px; border-radius: 5px; object-fit: cover; }

.filter-divider { width: 1px; height: 24px; background: $border; }

@media (max-width: 768px) {
  .search-filters { flex-direction: column; align-items: flex-start; gap: 12px; }
  .filter-divider { display: none; }
}
</style>
