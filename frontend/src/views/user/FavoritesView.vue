<template>
  <div class="favorites-view">
    <!-- Header -->
    <div class="page-header">
      <h2 class="page-title">我的收藏</h2>
      <span class="page-count" v-if="favStore.items.length > 0">{{ favStore.items.length }} 个收藏</span>
    </div>

    <!-- Empty state -->
    <div v-if="favStore.items.length === 0" class="empty-state">
      <div class="empty-icon-wrap">
        <svg viewBox="0 0 64 64" fill="none" width="80" height="80">
          <path d="M10.7 17.1a12 12 0 0117 0L32 21.4l4.3-4.3a12 12 0 0117 17L32 55.3 10.7 34.1a12 12 0 010-17z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <h3>还没有收藏</h3>
      <p>在探索页面浏览景点、酒店、餐厅，<br/>点击收藏即可添加到这里</p>
      <router-link to="/search" class="go-explore-btn">
        <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/></svg>
        去探索
      </router-link>
    </div>

    <!-- Favorites grid -->
    <div v-else class="fav-grid">
      <div v-for="poi in favStore.items" :key="poi.id" class="fav-card" @click="showDetail(poi)">
        <!-- Cover -->
        <div class="fav-card-cover" :style="{ background: coverGradient(poi.type) }">
          <div class="fav-cover-pattern"></div>
          <img class="fav-cover-icon" :src="coverIconImage(poi.type)" :alt="typeLabel(poi.type)" />
          <button class="fav-remove-btn" @click.stop="favStore.removeFavorite(poi.id)" title="取消收藏">
            <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/></svg>
          </button>
        </div>

        <!-- Body -->
        <div class="fav-card-body">
          <div class="fav-card-top">
            <span class="fav-type-tag">{{ typeLabel(poi.type) }}</span>
            <span class="fav-rating" v-if="poi.rating">
              <svg viewBox="0 0 16 16" fill="currentColor" width="12" height="12"><path d="M7.24 2.34c.23-.7 1.29-.7 1.52 0l.86 2.63c.08.26.3.44.57.44h2.77c.77 0 1.1.99.47 1.45l-2.24 1.63a.6.6 0 00-.22.67l.86 2.63c.24.74-.6 1.35-1.23.9L8 11.06a.6.6 0 00-.7 0l-2.24 1.63c-.63.46-1.47-.16-1.23-.9l.86-2.63a.6.6 0 00-.22-.67L2.23 7.4c-.63-.46-.3-1.45.47-1.45h2.77a.6.6 0 00.57-.44l.86-2.63z"/></svg>
              {{ poi.rating.toFixed(1) }}
            </span>
          </div>
          <h4 class="fav-card-name">{{ poi.name }}</h4>
          <p class="fav-card-location" v-if="poi.address || poi.city">
            <svg viewBox="0 0 16 16" fill="currentColor" width="12" height="12"><path fill-rule="evenodd" d="M4.04 3.24a5.6 5.6 0 017.92 7.92L8 15.12l-3.96-3.96a5.6 5.6 0 010-7.92zM8 8.8a1.6 1.6 0 100-3.2 1.6 1.6 0 000 3.2z" clip-rule="evenodd"/></svg>
            {{ poi.city || '' }}{{ poi.district ? ' ' + poi.district + '区' : '' }}
          </p>
          <div class="fav-card-bottom">
            <span class="fav-price">{{ poi.price > 0 ? `¥${poi.price}` : '免费' }}</span>
            <span class="fav-tags" v-if="poi.tags?.length">{{ poi.tags.slice(0, 2).join(' · ') }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Detail Panel -->
    <Teleport to="body">
      <transition name="panel-slide">
        <div v-if="detailVisible && detailPoi" class="detail-overlay" @click.self="detailVisible = false">
          <div class="detail-panel">
            <button class="detail-close" @click="detailVisible = false" aria-label="关闭">
              <svg viewBox="0 0 20 20" fill="currentColor" width="20" height="20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
            </button>

            <div class="detail-hero" :style="{ background: coverGradient(detailPoi.type) }">
              <div class="detail-hero-pattern"></div>
              <!-- Type-specific decorative scenery -->
              <div class="detail-hero-scenery" v-if="detailPoi">
                <svg v-if="detailPoi.type === 'attraction'" class="scenery-svg" viewBox="0 0 520 220" preserveAspectRatio="xMidYMax slice">
                  <defs><linearGradient id="sunGlow2" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="rgba(255,255,255,0.18)"/><stop offset="100%" stop-color="rgba(255,255,255,0)"/></linearGradient></defs>
                  <circle cx="430" cy="45" r="40" fill="url(#sunGlow2)"/>
                  <circle cx="430" cy="45" r="18" fill="rgba(255,255,255,0.12)"/>
                  <polygon points="0,220 60,70 130,130 210,35 290,110 380,55 460,140 520,80 520,220" fill="rgba(255,255,255,0.05)"/>
                  <polygon points="0,220 90,95 160,155 250,75 330,135 420,70 520,220" fill="rgba(255,255,255,0.035)"/>
                  <polygon points="0,220 130,140 210,170 310,120 430,160 520,130 520,220" fill="rgba(255,255,255,0.025)"/>
                </svg>
                <svg v-if="detailPoi.type === 'hotel'" class="scenery-svg" viewBox="0 0 520 220" preserveAspectRatio="xMidYMax slice">
                  <circle cx="40" cy="25" r="1.2" fill="rgba(255,255,255,0.25)"/><circle cx="130" cy="40" r="1" fill="rgba(255,255,255,0.2)"/><circle cx="280" cy="20" r="1.3" fill="rgba(255,255,255,0.3)"/><circle cx="400" cy="35" r="0.8" fill="rgba(255,255,255,0.2)"/><circle cx="480" cy="18" r="1.1" fill="rgba(255,255,255,0.25)"/>
                  <rect x="15" y="95" width="55" height="125" rx="2" fill="rgba(255,255,255,0.04)"/>
                  <rect x="80" y="65" width="45" height="155" rx="2" fill="rgba(255,255,255,0.055)"/>
                  <rect x="140" y="105" width="60" height="115" rx="2" fill="rgba(255,255,255,0.04)"/>
                  <rect x="215" y="55" width="42" height="165" rx="2" fill="rgba(255,255,255,0.05)"/>
                  <rect x="275" y="85" width="58" height="135" rx="2" fill="rgba(255,255,255,0.04)"/>
                  <rect x="350" y="70" width="50" height="150" rx="2" fill="rgba(255,255,255,0.045)"/>
                  <rect x="415" y="98" width="55" height="122" rx="2" fill="rgba(255,255,255,0.035)"/>
                  <g fill="rgba(255,220,150,0.1)">
                    <rect x="90" y="75" width="4" height="3" rx="1"/><rect x="110" y="75" width="4" height="3" rx="1"/>
                    <rect x="90" y="85" width="4" height="3" rx="1"/><rect x="110" y="85" width="4" height="3" rx="1"/>
                    <rect x="225" y="65" width="4" height="3" rx="1"/><rect x="235" y="65" width="4" height="3" rx="1"/>
                    <rect x="225" y="75" width="4" height="3" rx="1"/>
                    <rect x="360" y="80" width="4" height="3" rx="1"/><rect x="370" y="80" width="4" height="3" rx="1"/>
                    <rect x="360" y="90" width="4" height="3" rx="1"/>
                  </g>
                </svg>
                <svg v-if="detailPoi.type === 'restaurant'" class="scenery-svg" viewBox="0 0 520 220" preserveAspectRatio="xMidYMax slice">
                  <circle cx="90" cy="70" r="55" fill="rgba(255,200,100,0.08)"/>
                  <circle cx="390" cy="100" r="70" fill="rgba(255,180,80,0.06)"/>
                  <circle cx="250" cy="50" r="40" fill="rgba(255,220,150,0.05)"/>
                  <circle cx="70" cy="170" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="0.8"/>
                  <circle cx="70" cy="170" r="28" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="0.8"/>
                  <circle cx="440" cy="150" r="55" fill="none" stroke="rgba(255,255,255,0.045)" stroke-width="0.8"/>
                  <circle cx="440" cy="150" r="32" fill="none" stroke="rgba(255,255,255,0.035)" stroke-width="0.8"/>
                  <path d="M0,110 Q130,50 260,90 Q390,45 520,80" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="1"/>
                </svg>
              </div>
              <div class="detail-hero-content">
                <img class="detail-hero-icon" :src="coverIconImage(detailPoi.type)" :alt="typeLabel(detailPoi.type)" />
                <h2 class="detail-hero-name">{{ detailPoi.name }}</h2>
                <span class="detail-hero-type">{{ typeLabel(detailPoi.type) }}</span>
              </div>
            </div>

            <div class="detail-body-scroll">
              <div class="detail-body-inner">
                <div class="detail-stats">
                  <div class="detail-stat" v-if="detailPoi.rating">
                    <div class="stat-icon-wrap stat-icon-star">
                      <svg viewBox="0 0 20 20" fill="currentColor" width="22" height="22"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                    </div>
                    <div><span class="stat-value">{{ detailPoi.rating.toFixed(1) }}</span><span class="stat-label">评分</span></div>
                  </div>
                  <div class="detail-stat">
                    <div class="stat-icon-wrap stat-icon-coin">
                      <svg viewBox="0 0 20 20" fill="currentColor" width="22" height="22"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 000 2h4a1 1 0 110 2H7a1 1 0 100 2h4a3 3 0 002.683-4.133A3 3 0 0011 7H7a1 1 0 000 2h4a1 1 0 110 2H7z" clip-rule="evenodd"/></svg>
                    </div>
                    <div><span class="stat-value">{{ detailPoi.price > 0 ? `¥${detailPoi.price}` : '免费' }}</span><span class="stat-label">参考价格</span></div>
                  </div>
                  <div class="detail-stat" v-if="detailPoi.popularity_score">
                    <div class="stat-icon-wrap stat-icon-fire">
                      <svg viewBox="0 0 20 20" fill="currentColor" width="22" height="22"><path fill-rule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985 1.348-2.467-.363.59-.686 1.03-.903 1.47.27-.02.554-.05.847-.098.544-.09 1.17-.23 1.853-.507a1 1 0 00.604-1.264c-.52-1.643-1.65-2.637-2.487-3.318z" clip-rule="evenodd"/></svg>
                    </div>
                    <div><span class="stat-value">{{ (detailPoi.popularity_score / 10).toFixed(1) }}</span><span class="stat-label">热度</span></div>
                  </div>
                </div>

                <div class="detail-stars-row" v-if="detailPoi.rating">
                  <div class="stars-visual">
                    <span v-for="i in 5" :key="i" class="star-icon" :class="{ filled: i <= Math.round(detailPoi.rating), half: i === Math.ceil(detailPoi.rating) && detailPoi.rating % 1 >= 0.25 && detailPoi.rating % 1 < 0.75 }">
                      <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                    </span>
                    <span class="stars-text">{{ detailPoi.rating.toFixed(1) }} 分</span>
                  </div>
                </div>

                <div class="detail-section" v-if="detailPoi.address || detailPoi.city">
                  <div class="section-header">
                    <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
                    <span>位置信息</span>
                  </div>
                  <p class="section-text">{{ detailPoi.address || '' }}{{ detailPoi.address && detailPoi.city ? '，' : '' }}{{ detailPoi.city || '' }}{{ detailPoi.district ? ' ' + detailPoi.district + '区' : '' }}</p>
                </div>

                <div class="detail-section" v-if="detailPoi.opening_hours">
                  <div class="section-header">
                    <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/></svg>
                    <span>开放时间</span>
                  </div>
                  <p class="section-text">{{ detailPoi.opening_hours }}</p>
                </div>

                <div class="detail-section" v-if="detailPoi.description">
                  <div class="section-header">
                    <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm3 1h6v1.5H7V5zm0 3h6v1.5H7V8zm0 3h4v1.5H7V11z" clip-rule="evenodd"/></svg>
                    <span>详细介绍</span>
                  </div>
                  <div class="section-desc-box"><p>{{ detailPoi.description }}</p></div>
                </div>

                <div class="detail-section" v-if="detailPoi.tags?.length">
                  <div class="section-header">
                    <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M17.707 9.293a1 1 0 010 1.414l-7 7a1 1 0 01-1.414 0l-7-7A.997.997 0 012 10V5a3 3 0 013-3h5c.256 0 .512.098.707.293l7 7zM5 6a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"/></svg>
                    <span>特色标签</span>
                  </div>
                  <div class="detail-tags-row">
                    <span v-for="t in detailPoi.tags" :key="t" class="detail-tag-chip">{{ t }}</span>
                  </div>
                </div>

                <div class="detail-actions">
                  <button class="action-btn action-btn-primary">
                    <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/></svg>
                    加入行程
                  </button>
                  <button class="action-btn action-btn-secondary favorited" @click="detailPoi && favStore.toggleFavorite(detailPoi)">
                    <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/></svg>
                    已收藏
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useFavoritesStore } from '@/stores/favorites'
import type { POIResult } from '@/types/search'

const favStore = useFavoritesStore()
const detailVisible = ref(false)
const detailPoi = ref<POIResult | null>(null)

const typeLabel = (t: string) => ({ attraction: '景点', hotel: '酒店', restaurant: '餐厅' } as Record<string, string>)[t] || t
const coverGradient = (t: string) => ({ attraction: 'linear-gradient(160deg, #0A4F5C 0%, #0D7377 30%, #14919B 60%, #0D7377 100%)', hotel: 'linear-gradient(160deg, #1A0533 0%, #2D1B4E 30%, #4A2066 60%, #2D1B4E 100%)', restaurant: 'linear-gradient(160deg, #3D1C00 0%, #6B2F00 30%, #8B4513 60%, #5C2800 100%)' } as Record<string, string>)[t] || 'linear-gradient(160deg, #1a1a2e, #16213e, #0f3460)'
const coverEmoji = (t: string) => ({ attraction: '🏛️', hotel: '🏨', restaurant: '🍽️' } as Record<string, string>)[t] || '📍'
const coverIconImage = (t: string) => ({ attraction: '/assets/poi/type_attraction.png', hotel: '/assets/poi/type_hotel.png', restaurant: '/assets/poi/type_restaurant.png' } as Record<string, string>)[t] || '/assets/poi/type_attraction.png'

function showDetail(poi: POIResult) { detailPoi.value = poi; detailVisible.value = true }
</script>

<style scoped lang="scss">
$bg-deep: #0a0e1a;
$bg-card: #111827;
$bg-elevated: #1a2235;
$brand-amber: #f59e0b;
$text-primary: #f1f5f9;
$text-secondary: #94a3b8;
$text-muted: #64748b;
$border: #1e293b;

.favorites-view { padding: 0; }

.page-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 28px;
}
.page-title { font-size: 22px; font-weight: 700; color: $text-primary; margin: 0; }
.page-count { font-size: 13px; color: $text-muted; }

// Empty state
.empty-state {
  text-align: center; padding: 80px 20px; color: $text-secondary;
}
.empty-icon-wrap {
  width: 96px; height: 96px; border-radius: 50%;
  background: rgba(239,68,68,0.08); margin: 0 auto 24px;
  display: flex; align-items: center; justify-content: center;
  color: $text-muted;
}
.empty-state h3 { font-size: 18px; color: $text-primary; margin: 0 0 8px; }
.empty-state p { margin: 0 0 24px; font-size: 14px; line-height: 1.7; }
.go-explore-btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 28px; border-radius: 12px;
  background: linear-gradient(135deg, #fbbf24, #f59e0b); color: #0f172a;
  font-size: 14px; font-weight: 600; text-decoration: none;
  box-shadow: 0 4px 16px rgba(245,158,11,0.25);
  transition: all 0.25s;
  &:hover { transform: translateY(-1px); box-shadow: 0 6px 24px rgba(245,158,11,0.35); }
}

// Favorites grid
.fav-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 18px;
}
.fav-card {
  background: $bg-card; border: 1px solid $border; border-radius: 16px;
  overflow: hidden; cursor: pointer; transition: all 0.3s ease;
  &:hover { border-color: $brand-amber; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
}
.fav-card-cover {
  position: relative; height: 120px; display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}
.fav-cover-pattern {
  position: absolute; inset: 0; opacity: 0.16;
  background-image:
    radial-gradient(ellipse 180px 140px at 20% 30%, rgba(255,255,255,0.14) 0%, transparent 60%),
    radial-gradient(ellipse 160px 120px at 80% 70%, rgba(255,255,255,0.1) 0%, transparent 55%),
    radial-gradient(circle at 10px 10px, rgba(255,255,255,0.1) 0.5px, transparent 0.5px);
  background-size: auto, auto, 24px 24px;
}
.fav-cover-icon { width: 56px; height: 56px; border-radius: 14px; object-fit: cover; position: relative; z-index: 1; filter: drop-shadow(0 4px 10px rgba(0,0,0,0.3)); }
.fav-remove-btn {
  position: absolute; top: 10px; right: 10px;
  width: 32px; height: 32px; border-radius: 50%; border: none;
  background: rgba(0,0,0,0.35); color: #ef4444;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; opacity: 0; transition: all 0.25s;
  &:hover { background: rgba(239,68,68,0.3); }
}
.fav-card:hover .fav-remove-btn { opacity: 1; }

.fav-card-body { padding: 16px; }
.fav-card-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.fav-type-tag {
  padding: 2px 10px; border-radius: 10px; font-size: 11px; font-weight: 600;
  background: rgba(245,158,11,0.1); color: $brand-amber;
}
.fav-rating {
  font-size: 12px; font-weight: 600; color: $brand-amber;
  display: flex; align-items: center; gap: 3px;
}
.fav-card-name { font-size: 16px; font-weight: 700; color: $text-primary; margin: 0 0 6px; }
.fav-card-location {
  font-size: 12px; color: $text-muted; margin: 0 0 12px;
  display: flex; align-items: center; gap: 4px;
}
.fav-card-bottom { display: flex; align-items: center; justify-content: space-between; }
.fav-price { font-size: 15px; font-weight: 700; color: #10b981; }
.fav-tags { font-size: 12px; color: $text-muted; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 50%; }

// Detail Panel (same as SearchView)
.detail-overlay {
  position: fixed; inset: 0; z-index: 2000;
  background: rgba(0,0,0,0.6); backdrop-filter: blur(8px);
  display: flex; justify-content: flex-end;
}
.detail-panel {
  width: 100%; max-width: 520px; height: 100%;
  background: $bg-card; display: flex; flex-direction: column;
  overflow: hidden; box-shadow: -8px 0 40px rgba(0,0,0,0.5);
}
.detail-close {
  position: absolute; top: 16px; right: 16px; z-index: 10;
  width: 36px; height: 36px; border-radius: 50%; border: none;
  background: rgba(0,0,0,0.35); color: #fff;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; backdrop-filter: blur(6px);
  transition: all 0.25s;
  &:hover { background: rgba(0,0,0,0.5); transform: rotate(90deg); }
}
.detail-hero {
  position: relative; flex-shrink: 0;
  padding: 56px 28px 32px; overflow: hidden;
  min-height: 200px; display: flex; align-items: flex-end;
}
.detail-hero-pattern {
  position: absolute; inset: 0; opacity: 0.12;
  background-image:
    radial-gradient(ellipse 200px 140px at 25% 30%, rgba(255,255,255,0.08) 0%, transparent 60%),
    radial-gradient(ellipse 180px 120px at 75% 60%, rgba(255,255,255,0.06) 0%, transparent 55%),
    radial-gradient(circle at 14px 14px, rgba(255,255,255,0.08) 0.5px, transparent 0.5px);
  background-size: auto, auto, 32px 32px;
}
.detail-hero-scenery {
  position: absolute; inset: 0; z-index: 0; pointer-events: none;
}
.scenery-svg {
  position: absolute; bottom: 0; left: 0;
  width: 100%; height: 100%;
}
.detail-hero-content { position: relative; z-index: 1; }
.detail-hero-icon { width: 72px; height: 72px; display: block; margin-bottom: 12px; border-radius: 16px; object-fit: cover; filter: drop-shadow(0 6px 16px rgba(0,0,0,0.35)); }
.detail-hero-name { font-size: 26px; font-weight: 800; color: #fff; margin: 0 0 6px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }
.detail-hero-type {
  display: inline-block; padding: 4px 14px; border-radius: 20px;
  font-size: 12px; font-weight: 600; color: #fff;
  background: rgba(255,255,255,0.18); backdrop-filter: blur(6px);
  letter-spacing: 0.5px;
}
.detail-body-scroll { flex: 1; overflow-y: auto; -webkit-overflow-scrolling: touch; }
.detail-body-inner { padding: 24px 28px 40px; }
.detail-stats { display: flex; gap: 12px; margin-bottom: 20px; }
.detail-stat {
  flex: 1; display: flex; align-items: center; gap: 12px;
  padding: 16px; background: $bg-elevated; border-radius: 14px;
  border: 1px solid $border;
}
.stat-icon-wrap {
  width: 44px; height: 44px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.stat-icon-star { background: linear-gradient(135deg, rgba(245,158,11,0.2), rgba(245,158,11,0.08)); color: #f59e0b; }
.stat-icon-coin { background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(16,185,129,0.08)); color: #10b981; }
.stat-icon-fire { background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(239,68,68,0.08)); color: #ef4444; }
.stat-value { display: block; font-size: 18px; font-weight: 700; color: $text-primary; line-height: 1.2; }
.stat-label { display: block; font-size: 11px; color: $text-muted; margin-top: 2px; }
.detail-stars-row { margin-bottom: 20px; }
.stars-visual { display: flex; align-items: center; gap: 3px; }
.star-icon { color: $border; display: flex; &.filled { color: #f59e0b; } &.half { color: #f59e0b; opacity: 0.5; } }
.stars-text { font-size: 13px; font-weight: 600; color: $brand-amber; margin-left: 8px; }
.detail-section { margin-bottom: 20px; }
.section-header { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; color: $brand-amber; font-size: 13px; font-weight: 600; }
.section-text { font-size: 14px; color: $text-secondary; line-height: 1.7; margin: 0; }
.section-desc-box { padding: 16px; border-radius: 12px; background: $bg-elevated; border: 1px solid $border;
  p { margin: 0; font-size: 14px; color: $text-secondary; line-height: 1.85; }
}
.detail-tags-row { display: flex; flex-wrap: wrap; gap: 8px; }
.detail-tag-chip {
  padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;
  color: $brand-amber; background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.15);
}
.detail-actions { display: flex; gap: 12px; margin-top: 28px; padding-top: 24px; border-top: 1px solid $border; }
.action-btn {
  flex: 1; display: flex; align-items: center; justify-content: center; gap: 8px;
  padding: 14px 20px; border-radius: 14px; border: none;
  font-size: 14px; font-weight: 600; cursor: pointer; font-family: inherit;
  transition: all 0.25s ease;
}
.action-btn-primary {
  background: linear-gradient(135deg, #fbbf24, #f59e0b); color: #0f172a;
  box-shadow: 0 4px 16px rgba(245,158,11,0.25);
  &:hover { transform: translateY(-1px); box-shadow: 0 6px 24px rgba(245,158,11,0.35); }
}
.action-btn-secondary {
  background: $bg-elevated; color: $text-secondary; border: 1px solid $border;
  &:hover { color: $brand-amber; border-color: rgba(245,158,11,0.3); }
  &.favorited {
    color: #ef4444; border-color: rgba(239,68,68,0.25); background: rgba(239,68,68,0.08);
    &:hover { color: #f87171; border-color: rgba(239,68,68,0.4); background: rgba(239,68,68,0.12); }
  }
}

.panel-slide-enter-active { transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1); }
.panel-slide-leave-active { transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); }
.panel-slide-enter-from, .panel-slide-leave-to {
  .detail-overlay { opacity: 0; }
  .detail-panel { transform: translateX(100%); }
}

@media (max-width: 540px) {
  .detail-panel { max-width: 100%; }
  .detail-hero { padding: 48px 20px 28px; min-height: 170px; }
  .detail-body-inner { padding: 20px; }
  .detail-stats { flex-direction: column; gap: 8px; }
  .fav-grid { grid-template-columns: 1fr; }
}
</style>
