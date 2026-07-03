<template>
  <Teleport to="body">
    <div class="map-overlay" @click.self="$emit('close')">
      <div class="map-popup">
        <!-- 头部 -->
        <div class="map-header">
          <div class="map-header-left">
            <svg class="header-icon" viewBox="0 0 20 20" fill="currentColor" width="18" height="18"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
            <span class="map-title">{{ name || '活动位置' }}</span>
            <span v-if="selectedAddress" class="address-tag">{{ selectedAddress }}</span>
          </div>
          <button class="close-btn" @click="$emit('close')">
            <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
          </button>
        </div>

        <!-- 搜索栏 -->
        <div class="search-bar">
          <svg class="search-icon" viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/></svg>
          <input
            ref="searchInput"
            v-model="searchKeyword"
            placeholder="搜索地点、地址..."
            class="search-input"
            @input="onSearchInput"
          />
          <div v-if="showSuggestions && suggestions.length > 0" class="suggestions-dropdown">
            <div
              v-for="(item, idx) in suggestions"
              :key="idx"
              class="suggestion-item"
              @click="selectSuggestion(item)"
            >
              <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14" style="flex-shrink:0;opacity:0.4;color:var(--color-warm-brown,#A68B7A)"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
              <span>{{ item.name }}</span><span class="sug-address">{{ item.address || item.district }}</span>
            </div>
          </div>
        </div>

        <!-- 地图区域 -->
        <div class="map-container" ref="mapContainerRef">
          <!-- 地图渲染在这里 -->
        </div>

        <!-- 坐标信息 & 操作按钮 -->
        <div class="map-toolbar">
          <div class="coords-info" v-if="markerPos.lat !== 0">
            <svg viewBox="0 0 20 20" fill="currentColor" width="13" height="13"><path d="M10 2a6 6 0 00-6 6c0 4.5 6 10 6 10s6-5.5 6-10a6 6 0 00-6-6zm0 8a2 2 0 110-4 2 2 0 010 4z"/></svg>
            <span>{{ markerPos.lat.toFixed(4) }}, {{ markerPos.lng.toFixed(4) }}</span>
          </div>
          <div class="toolbar-actions">
            <button class="tool-btn locate-btn" :class="{ loading: locating }" @click="locateCurrentPosition">
              <svg v-if="!locating" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15"><circle cx="12" cy="12" r="3"/><path d="M12 2v4m0 12v4m10-10h-4M6 12H2m15.07-7.07l-2.83 2.83M9.76 14.24l-2.83 2.83m11.31 0l-2.83-2.83M9.76 9.76L6.93 6.93"/></svg>
              <svg v-else class="spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15"><path d="M21 12a9 9 0 11-6.22-8.56"/></svg>
              {{ locating ? '定位中...' : '定位' }}
            </button>
            <button class="tool-btn confirm-btn" :disabled="!hasLocation" @click="confirmLocation">
              <svg viewBox="0 0 20 20" fill="currentColor" width="15" height="15"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              确认位置
            </button>
          </div>
        </div>

        <!-- 周边推荐 -->
        <div class="nearby-section" v-if="nearbyItems.length > 0 && hasLocation">
          <div class="nearby-header">
            <svg viewBox="0 0 20 20" fill="currentColor" width="15" height="15"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
            <h4>周边推荐</h4>
          </div>
          <div class="nearby-list">
            <div
              v-for="(item, index) in nearbyItems"
              :key="index"
              class="nearby-item"
              @click="selectNearby(item)"
            >
              <span class="nearby-icon">{{ item.icon }}</span>
              <div class="nearby-info">
                <span class="nearby-name">{{ item.name }}</span>
                <span class="nearby-dist">{{ item.distance }}</span>
              </div>
              <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14" style="opacity:0.25;color:var(--color-warm-brown,#A68B7A)"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/></svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'

declare global {
  interface Window {
    AMap: any
  }
}

const props = defineProps<{
  lat: number
  lng: number
  name?: string
}>()

const emit = defineEmits<{
  close: []
  select: [lat: number, lng: number, address: string]
}>()

// ── Refs ──
const mapContainerRef = ref<HTMLDivElement>()
const searchInput = ref<HTMLInputElement>()

// ── State ──
let mapInstance: any = null
let markerInstance: any = null
let geocoder: any = null
let placeSearch: any = null

const markerPos = reactive({ lat: props.lat || 0, lng: props.lng || 0 })
const selectedAddress = ref('')
const searchKeyword = ref('')
const showSuggestions = ref(false)
const suggestions = ref<any[]>([])
const locating = ref(false)
const nearbyItems = ref<any[]>([])

// 计算属性
const hasLocation = ref(markerPos.lat !== 0 && markerPos.lng !== 0)

// ── 初始化地图 ──
onMounted(async () => {
  await nextTick()
  initMap()
})

function initMap() {
  if (!window.AMap || !mapContainerRef.value) return

  const defaultCenter = (props.lat && props.lng)
    ? [props.lng, props.lat]
    : [116.397428, 39.90923] // 默认北京天安门

  mapInstance = new window.AMap.Map(mapContainerRef.value, {
    zoom: 15,
    center: defaultCenter,
    viewMode: '2D',
    mapStyle: 'amap://styles/normal', // 使用标准样式，后续可换大地素雅风
    resizeEnable: true,
  })

  // 初始位置有值则添加标记
  if (props.lat && props.lng) {
    addMarker(props.lat, props.lng)
  }

  // 点击地图选点
  mapInstance.on('click', (e: any) => {
    const lat = e.lnglat.getLat()
    const lng = e.lnglat.getLng()
    addMarker(lat, lng)
    reverseGeocode(lat, lng)
    fetchNearestPOI(lat, lng)
  })

  // 初始化 Geocoder（逆地理编码）
  geocoder = new window.AMap.Geocoder({
    city: '全国',
    radius: 500,
  })

  // 初始化 PlaceSearch（POI 搜索）
  placeSearch = new window.AMap.PlaceSearch({
    city: '全国',
    pageSize: 6,
  })

  // 如果初始有坐标，做逆地理编码获取地址
  if (props.lat && props.lng) {
    reverseGeocode(props.lat, props.lng)
    fetchNearestPOI(props.lat, props.lng)
    searchNearby(props.lat, props.lng)
  }
}

function addMarker(lat: number, lng: number) {
  // 移除旧标记
  if (markerInstance) {
    mapInstance.remove(markerInstance)
  }

  markerInstance = new window.AMap.Marker({
    position: [lng, lat],
    animation: 'AMAP_ANIMATION_BOUNCE',
    offset: new window.AMap.Pixel(-13, -30),
  })
  mapInstance.add(markerInstance)

  markerPos.lat = lat
  markerPos.lng = lng
  hasLocation.value = true
}

// ── 逆地理编码 + 最近POI名称 ──
function reverseGeocode(lat: number, lng: number) {
  if (!geocoder) return

  // 同时执行：逆地理编码 + 周边POI搜索（取最近的）
  // 先清空旧值
  selectedAddress.value = ''

  geocoder.getAddress([lng, lat], (status: string, result: any) => {
    if (status === 'complete' && result.regeocode) {
      const rg = result.regeocode

      // 优先使用 AOI（兴趣区域/建筑）或交叉路名
      let addr = ''
      if (rg.aois && rg.aois.length > 0) {
        addr = rg.aois[0].name
      }
      if (!addr && rg.crosses && rg.crosses.length > 0) {
        const c = rg.crosses[0]
        if (c.cross_name) addr = c.cross_name
        else addr = `${c.first_road_name || ''}与${c.second_road_name || ''}路口`.replace(/^与|与$/g, '')
      }

      // 最终兜底用完整地址
      if (!addr) {
        addr = rg.formattedAddress
      }

      selectedAddress.value = addr
    }
  })
}

// 点击地图时同时搜索最近POI
function fetchNearestPOI(lat: number, lng: number) {
  if (!placeSearch) return
  placeSearch.searchNearBy('', [lng, lat], 300, { pageSize: 1 }, (_status: string, result: any) => {
    if (result?.poiList?.pois?.length > 0) {
      const poi = result.poiList.pois[0]
      // 用最近的POI名称覆盖地址显示（更直观）
      selectedAddress.value = poi.name
    }
  })
}

// ── 当前定位 ──
async function locateCurrentPosition() {
  if (!window.AMap || !mapInstance) return

  locating.value = true
  try {
    const geolocation = new window.AMap.Geolocation({
      enableHighAccuracy: true,
      timeout: 8000,
      showButton: false,
      showMarker: false,
      zoomToAccuracy: true,
    })

    geolocation.getCurrentPosition((status: string, result: any) => {
      locating.value = false
      if (status === 'complete') {
        const lat = result.position.getLat()
        const lng = result.position.getLng()
        addMarker(lat, lng)
        reverseGeocode(lat, lng)
        fetchNearestPOI(lat, lng)
        mapInstance.setZoomAndCenter(17, [lng, lat], false, 300)
        searchNearby(lat, lng)
      } else {
        // 高德定位失败，尝试浏览器原生定位
        browserGeolocation()
      }
    }, () => {
      locating.value = false
      browserGeolocation()
    })
  } catch {
    locating.value = false
  }
}

function browserGeolocation() {
  if (!navigator.geolocation) return
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const lat = pos.coords.latitude
      const lng = pos.coords.longitude
      addMarker(lat, lng)
      reverseGeocode(lat, lng)
      fetchNearestPOI(lat, lng)
      mapInstance.setZoomAndCenter(17, [lng, lat], false, 300)
      searchNearby(lat, lng)
    },
    () => {
      console.warn('[MapPopup] 定位失败')
    },
    { enableHighAccuracy: true, timeout: 8000 }
  )
}

// ── 搜索 ──
let searchTimer: ReturnType<typeof setTimeout> | null = null

function onSearchInput() {
  const keyword = searchKeyword.value.trim()
  if (!keyword) {
    showSuggestions.value = false
    suggestions.value = []
    return
  }

  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    doSearch(keyword)
  }, 350)
}

function doSearch(keyword: string) {
  if (!placeSearch) return
  placeSearch.search(keyword, (status: string, result: any) => {
    if (status === 'complete' && result.poiList) {
      suggestions.value = result.poiList.pois.slice(0, 6).map((p: any) => ({
        name: p.name,
        address: p.address,
        district: p.cityname || '',
        location: p.location,
      }))
      showSuggestions.value = suggestions.value.length > 0
    }
  })
}

function selectSuggestion(item: any) {
  if (!item.location) return
  const lng = item.location.getLng()
  const lat = item.location.getLat()
  addMarker(lat, lng)
  mapInstance.setZoomAndCenter(16, [lng, lat], false, 400)
  selectedAddress.value = item.name
  searchKeyword.value = ''
  showSuggestions.value = false
  fetchNearestPOI(lat, lng)
  searchNearby(lat, lng)
}

// ── 周边搜索 ──
function searchNearby(lat: number, lng: number) {
  if (!placeSearch) return
  const types = ['餐饮服务', '购物服务', '交通设施服务', '风景名胜']
  const icons = ['🍜', '🛒', '🚇', '🏞️']
  
  let count = 0
  types.forEach((type, i) => {
    placeSearch.searchNearBy(type, [lng, lat], 1500, { pageSize: 1 }, (_status: string, result: any) => {
      count++
      if (result?.poiList?.pois?.length > 0) {
        const poi = result.poiList.pois[0]
        const dist = Math.round(poi.distance || 0)
        nearbyItems.value.push({
          name: poi.name,
          icon: icons[i],
          distance: dist < 1000 ? `${dist}m` : `${(dist / 1000).toFixed(1)}km`,
          location: poi.location,
        })
        nearbyItems.value.sort((a, b) => {
          const da = parseInt(a.distance), db = parseInt(b.distance)
          return da - db
        })
      }
    })
  })
}

function selectNearby(item: any) {
  if (!item.location) return
  const lng = item.location.getLng()
  const lat = item.location.getLat()
  addMarker(lat, lng)
  mapInstance.setZoomAndCenter(16, [lng, lat], false, 400)
  reverseGeocode(lat, lng)
  fetchNearestPOI(lat, lng)
  selectedAddress.value = item.name
  searchNearby(lat, lng)
}

// ── 确认选择 ──
function confirmLocation() {
  if (!hasLocation.value) return
  // 兜底：如果地址还没加载出来，用坐标作为地址
  const addr = selectedAddress.value
    || `${markerPos.lat.toFixed(4)}, ${markerPos.lng.toFixed(4)}`
  emit('select', markerPos.lat, markerPos.lng, addr)
  emit('close')
}

// ── 清理 ──
onBeforeUnmount(() => {
  if (mapInstance) {
    mapInstance.destroy()
    mapInstance = null
  }
  if (searchTimer) clearTimeout(searchTimer)
})

// 监听外部 props 变化重新初始化
watch(() => [props.lat, props.lng], () => {
  if (props.lat && props.lng && mapInstance) {
    addMarker(props.lat, props.lng)
    mapInstance.setCenter([props.lng, props.lat])
    reverseGeocode(props.lat, props.lng)
    fetchNearestPOI(props.lat, props.lng)
  }
})
</script>

<style scoped lang="scss">
// ==========================================
// MapPopup — 大地素雅风 + 高德地图
// ==========================================

.map-overlay {
  position: fixed;
  inset: 0;
  background: rgba(61, 61, 61, 0.45);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(2px);
  padding: 20px;
}

.map-popup {
  width: 420px;
  max-height: 88vh;
  background: var(--color-warm-white, #FAF8F3);
  border-radius: 20px;
  box-shadow:
    0 20px 60px rgba(61, 61, 61, 0.2),
    0 0 0 1px rgba(166, 139, 122, 0.08);
  overflow-y: auto;
  display: flex;
  flex-direction: column;

  // 自定义滚动条
  &::-webkit-scrollbar { width: 5px; }
  &::-webkit-scrollbar-track { background: transparent; }
  &::-webkit-scrollbar-thumb { background: rgba(166,139,122,0.2); border-radius: 3px; }
}

// ── 头部 ──
.map-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 22px 14px;
  flex-shrink: 0;
}

.map-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.header-icon {
  color: var(--color-warm-brown, #A68B7A);
  opacity: 0.55;
  flex-shrink: 0;
}

.map-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text-primary, #3D3D3D);
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.address-tag {
  font-size: 11px;
  color: var(--color-warm-brown, #A68B7A);
  background: rgba(166, 139, 122, 0.09);
  padding: 2px 8px;
  border-radius: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 50%;
  background: rgba(166, 139, 122, 0.06);
  color: var(--color-text-secondary, #6B6B6B);
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;

  &:hover {
    background: rgba(166, 139, 122, 0.15);
    color: var(--color-warm-brown, #A68B7A);
  }
}

// ── 搜索栏 ──
.search-bar {
  position: relative;
  margin: 0 18px 12px;
  flex-shrink: 0;
}

.search-icon {
  position: absolute;
  left: 13px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-warm-brown, #A68B7A);
  opacity: 0.35;
  pointer-events: none;
}

.search-input {
  width: 100%;
  height: 42px;
  padding: 0 14px 0 38px;
  background: var(--color-cream, #FDFBF7);
  border: 1.5px solid rgba(166, 139, 122, 0.12);
  border-radius: 12px;
  color: var(--color-text-primary, #3D3D3D);
  font-size: 14px;
  font-family: inherit;
  outline: none;
  box-sizing: border-box;
  transition: all 0.25s ease;

  &::placeholder { color: #c5c0b7; }

  &:hover { border-color: rgba(166, 139, 122, 0.28); }

  &:focus {
    border-color: var(--color-warm-brown, #A68B7A);
    box-shadow: 0 0 0 3px rgba(166, 139, 122, 0.06);
  }
}

.suggestions-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  right: 0;
  background: var(--color-warm-white, #FAF8F3);
  border: 1.5px solid rgba(166, 139, 122, 0.12);
  border-radius: 12px;
  box-shadow: 0 8px 28px rgba(61, 61, 61, 0.1);
  z-index: 50;
  max-height: 220px;
  overflow-y: auto;
  padding: 6px;

  &::-webkit-scrollbar { width: 4px; }
  &::-webkit-scrollbar-thumb { background: rgba(166,139,122,0.2); border-radius: 2px; }
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  color: var(--color-text-primary, #3D3D3D);
  transition: all 0.15s;

  &:hover {
    background: rgba(166, 139, 122, 0.06);
  }
}

.sug-address {
  font-size: 11px;
  color: var(--color-text-secondary, #6B6B6B);
  margin-left: auto;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 120px;
}

// ── 地图容器 ──
.map-container {
  width: 100%;
  height: 280px;
  margin: 0 18px 12px;
  border-radius: 14px;
  overflow: hidden;
  border: 1.5px solid rgba(166, 139, 122, 0.1);
  flex-shrink: 0;
  background: #f0ebe3;

  // 覆盖高德地图默认 logo 和版权
  :deep(.amap-logo),
  :deep(.amap-copyright) {
    display: none !important;
  }
}

// ── 工具栏 ──
.map-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 18px 14px;
  gap: 12px;
  flex-shrink: 0;
}

.coords-info {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  color: var(--color-text-secondary, #6B6B6B);
  font-family: monospace;
  background: rgba(166, 139, 122, 0.06);
  padding: 4px 10px;
  border-radius: 8px;

  svg { opacity: 0.5; color: var(--color-warm-brown, #A68B7A); }
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tool-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  height: 34px;
  padding: 0 14px;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.25s ease;
  white-space: nowrap;

  &.disabled,
  &[disabled] {
    opacity: 0.35;
    cursor: not-allowed;
  }
}

.locate-btn {
  background: var(--color-oat, #F5F0E8);
  color: var(--color-warm-brown, #A68B7A);

  &:hover:not(.loading) {
    background: linear-gradient(135deg, var(--color-sage, #B8C4B8), #a8bca8);
    color: #fff;
  }

  &.loading { cursor: wait; }
}

.confirm-btn {
  background: linear-gradient(135deg, var(--color-warm-brown, #A68B7A), #8f7362);
  color: #fff;
  box-shadow: 0 2px 10px rgba(166, 139, 122, 0.25);

  &:hover:not([disabled]) {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(166, 139, 122, 0.35);
  }

  &:active:not([disabled]) {
    transform: translateY(0);
  }
}

// ── 周边 ──
.nearby-section {
  margin: 4px 18px 18px;
  padding-top: 12px;
  border-top: 1px solid rgba(166, 139, 122, 0.08);
  flex-shrink: 0;
}

.nearby-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 10px;

  svg { color: var(--color-sage, #B8C4B8); opacity: 0.7; }

  h4 {
    font-size: 13px;
    font-weight: 700;
    color: var(--color-text-primary, #3D3D3D);
    letter-spacing: 0.3px;
    margin: 0;
  }
}

.nearby-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.nearby-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: var(--color-cream, #FDFBF7);
  border: 1.5px solid rgba(166, 139, 122, 0.06);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    border-color: rgba(166, 139, 122, 0.18);
    background: #fff;
    transform: translateX(2px);
  }

  svg:last-child {
    margin-left: auto;
    flex-shrink: 0;
  }
}

.nearby-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.nearby-info {
  flex: 1;
  min-width: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.nearby-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary, #3D3D3D);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nearby-dist {
  font-size: 11px;
  color: var(--color-text-secondary, #6B6B6B);
  font-weight: 600;
  background: rgba(184, 196, 184, 0.15);
  padding: 1px 7px;
  border-radius: 6px;
  white-space: nowrap;
  flex-shrink: 0;
}

// ── 动画 ──
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.spin { animation: spin 0.8s linear infinite; }

// ── 响应式 ──
@media (max-width: 480px) {
  .map-overlay { padding: 10px; }
  .map-popup { width: 94vw; max-height: 92vh; }
  .map-container { height: 240px; }
}
</style>
