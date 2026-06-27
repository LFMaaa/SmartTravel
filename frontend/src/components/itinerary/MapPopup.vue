<template>
  <Teleport to="body">
    <div class="map-overlay" @click.self="$emit('close')">
      <div class="map-popup">
        <div class="map-header">
          <span class="map-title">{{ name || '活动位置' }}</span>
          <el-button text @click="$emit('close')">
            <el-icon :size="18"><Close /></el-icon>
          </el-button>
        </div>
        <div class="map-body">
          <!-- Static map placeholder: uses Amap static image API -->
          <div class="map-placeholder">
            <div class="map-pin">
              <el-icon :size="32" color="#F44336"><LocationFilled /></el-icon>
            </div>
            <div class="map-info">
              <div class="map-coords" v-if="lat && lng">
                📍 {{ lat.toFixed(4) }}, {{ lng.toFixed(4) }}
              </div>
              <div class="map-hint">点击查看大地图</div>
            </div>
          </div>

          <!-- Nearby recommendations -->
          <div class="nearby-section">
            <h4>周边推荐</h4>
            <div class="nearby-list">
              <div v-for="item in nearbyItems" :key="item.name" class="nearby-item">
                <span class="nearby-icon">{{ item.icon }}</span>
                <div class="nearby-info">
                  <span class="nearby-name">{{ item.name }}</span>
                  <span class="nearby-dist">{{ item.distance }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { LocationFilled, Close } from '@element-plus/icons-vue'

defineProps<{
  lat: number
  lng: number
  name?: string
}>()

defineEmits<{ close: [] }>()

// Mock nearby items
const nearbyItems = [
  { name: '附近餐厅', icon: '🍜', distance: '200m' },
  { name: '咖啡厅', icon: '☕', distance: '350m' },
  { name: '地铁站', icon: '🚇', distance: '500m' },
  { name: '便利店', icon: '🏪', distance: '150m' },
]
</script>

<style scoped lang="scss">
.map-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-popup {
  width: 360px;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
}

.map-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md) var(--space-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.map-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
}

.map-body {
  padding: var(--space-lg);
}

.map-placeholder {
  height: 200px;
  background: var(--color-bg-alt);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-lg);
  position: relative;
  overflow: hidden;
  border: 1px solid var(--color-border-light);

  // Grid pattern
  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(rgba(30,136,229,0.05) 1px, transparent 1px),
      linear-gradient(90deg, rgba(30,136,229,0.05) 1px, transparent 1px);
    background-size: 20px 20px;
  }
}

.map-pin {
  position: relative;
  z-index: 1;
  animation: float 3s ease-in-out infinite;
}

.map-info {
  position: relative;
  z-index: 1;
  text-align: center;
  margin-top: var(--space-sm);
}

.map-coords {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  font-family: monospace;
}

.map-hint {
  font-size: var(--font-size-xs);
  color: var(--color-primary);
  margin-top: 4px;
}

.nearby-section {
  h4 {
    font-size: var(--font-size-sm);
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: var(--space-sm);
  }
}

.nearby-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.nearby-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm);
  background: var(--color-bg);
  border-radius: var(--radius-sm);
}

.nearby-icon {
  font-size: 18px;
}

.nearby-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nearby-name {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
}

.nearby-dist {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

@media (max-width: 768px) {
  .map-popup {
    width: 90vw;
    max-height: 80vh;
    overflow-y: auto;
  }
}
</style>
