<template>
  <div class="search-view">
    <!-- Hero search area -->
    <div class="search-hero">
      <div class="search-hero-bg">
        <div class="hero-orb orb-a"></div>
        <div class="hero-orb orb-b"></div>
      </div>
      <div class="search-hero-content">
        <h1 class="search-title">探索目的地</h1>
        <p class="search-subtitle">搜索景点、酒店、餐厅，发现旅途中的精彩</p>
        <SearchBar @search="handleSearch" />
        <SearchFilters v-model="filters" @update:model-value="onFilterChange" />
      </div>
    </div>

    <!-- Results area -->
    <div class="search-body container">
      <div v-if="searched && !store.loading" class="results-stats">
        <span>
          搜索 "<strong>{{ lastKeyword }}</strong>"
          <template v-if="filters.city"> · {{ filters.city }}</template>
          <template v-if="filters.poi_type"> · {{ typeLabel(filters.poi_type) }}</template>
        </span>
        <span class="stats-count">共 {{ store.total }} 条结果</span>
      </div>

      <!-- Loading -->
      <div v-if="store.loading" class="results-grid">
        <div v-for="i in 6" :key="i" class="skeleton-card">
          <div class="sk-cover shimmer-bg"></div>
          <div class="sk-body">
            <div class="sk-title shimmer-bg"></div>
            <div class="sk-meta shimmer-bg"></div>
            <div class="sk-tags">
              <span class="sk-tag shimmer-bg"></span>
              <span class="sk-tag shimmer-bg"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Error -->
      <div v-else-if="searchError" class="error-state">
        <svg viewBox="0 0 20 20" fill="currentColor" width="48" height="48"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
        <h3>搜索服务暂不可用</h3>
        <p>{{ searchError }}</p>
        <button class="retry-btn" @click="retrySearch">重试</button>
      </div>

      <!-- Empty -->
      <div v-else-if="searched && store.results.length === 0" class="empty-state">
        <svg viewBox="0 0 20 20" fill="currentColor" width="48" height="48"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/></svg>
        <h3>未找到相关结果</h3>
        <p>试试其他关键词，或浏览下方热门推荐</p>
        <div class="quick-searches">
          <button v-for="q in quickSearches" :key="q" class="quick-chip" @click="handleSearch(q)">{{ q }}</button>
        </div>
      </div>

      <!-- Welcome -->
      <div v-else-if="!searched" class="welcome-state">
        <div class="welcome-grid">
          <div v-for="item in popularSearches" :key="item.label" class="welcome-chip" @click="showPoiDetail(item.poiData)">
            <div class="chip-image-wrap">
              <img class="chip-image" :src="item.image" :alt="item.label" loading="lazy" />
            </div>
            <span class="chip-label">{{ item.label }}</span>
            <span class="chip-desc">{{ item.desc }}</span>
          </div>
        </div>
      </div>

      <!-- Results -->
      <div v-else class="results-grid">
        <PoiCard v-for="item in store.results" :key="item.id" :poi="item" @click="showPoiDetail(item)" />
      </div>

      <!-- Pagination -->
      <div v-if="store.total > pageSize" class="pagination">
        <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="store.total" layout="prev, pager, next, total" background @current-change="handlePageChange" />
      </div>
    </div>

    <!-- POI Detail Fullscreen Panel -->
    <Teleport to="body">
      <transition name="panel-slide">
        <div v-if="detailVisible && detailPoi" class="detail-overlay" @click.self="detailVisible = false">
          <div class="detail-panel">
            <!-- Close button -->
            <button class="detail-close" @click="detailVisible = false" aria-label="关闭">
              <svg viewBox="0 0 20 20" fill="currentColor" width="20" height="20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
            </button>

            <!-- Hero Cover -->
            <div class="detail-hero" :style="{ background: coverGradient(detailPoi.type) }">
              <div class="detail-hero-pattern"></div>
              <!-- Type-specific decorative scenery -->
              <div class="detail-hero-scenery" v-if="detailPoi">
                <!-- 景点：山峦日落风景 -->
                <svg v-if="detailPoi.type === 'attraction'" class="scenery-svg" viewBox="0 0 520 220" preserveAspectRatio="xMidYMax slice">
                  <defs><linearGradient id="sunGlow" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="rgba(255,255,255,0.18)"/><stop offset="100%" stop-color="rgba(255,255,255,0)"/></linearGradient></defs>
                  <circle cx="430" cy="45" r="40" fill="url(#sunGlow)"/>
                  <circle cx="430" cy="45" r="18" fill="rgba(255,255,255,0.12)"/>
                  <polygon points="0,220 60,70 130,130 210,35 290,110 380,55 460,140 520,80 520,220" fill="rgba(255,255,255,0.05)"/>
                  <polygon points="0,220 90,95 160,155 250,75 330,135 420,70 520,220" fill="rgba(255,255,255,0.035)"/>
                  <polygon points="0,220 130,140 210,170 310,120 430,160 520,130 520,220" fill="rgba(255,255,255,0.025)"/>
                  <path d="M60,55 Q75,38 90,55 Q105,38 120,55 Q135,38 150,55" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
                  <path d="M330,30 Q345,18 360,30 Q375,18 390,30" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
                </svg>
                <!-- 酒店：城市夜景 -->
                <svg v-if="detailPoi.type === 'hotel'" class="scenery-svg" viewBox="0 0 520 220" preserveAspectRatio="xMidYMax slice">
                  <circle cx="40" cy="25" r="1.2" fill="rgba(255,255,255,0.25)"/><circle cx="130" cy="40" r="1" fill="rgba(255,255,255,0.2)"/><circle cx="280" cy="20" r="1.3" fill="rgba(255,255,255,0.3)"/><circle cx="400" cy="35" r="0.8" fill="rgba(255,255,255,0.2)"/><circle cx="480" cy="18" r="1.1" fill="rgba(255,255,255,0.25)"/><circle cx="210" cy="48" r="0.9" fill="rgba(255,255,255,0.18)"/>
                  <rect x="15" y="95" width="55" height="125" rx="2" fill="rgba(255,255,255,0.04)"/>
                  <rect x="80" y="65" width="45" height="155" rx="2" fill="rgba(255,255,255,0.055)"/>
                  <rect x="140" y="105" width="60" height="115" rx="2" fill="rgba(255,255,255,0.04)"/>
                  <rect x="215" y="55" width="42" height="165" rx="2" fill="rgba(255,255,255,0.05)"/>
                  <rect x="275" y="85" width="58" height="135" rx="2" fill="rgba(255,255,255,0.04)"/>
                  <rect x="350" y="70" width="50" height="150" rx="2" fill="rgba(255,255,255,0.045)"/>
                  <rect x="415" y="98" width="55" height="122" rx="2" fill="rgba(255,255,255,0.035)"/>
                  <rect x="480" y="88" width="40" height="132" rx="2" fill="rgba(255,255,255,0.03)"/>
                  <!-- 窗灯 -->
                  <g fill="rgba(255,220,150,0.1)">
                    <rect x="90" y="75" width="4" height="3" rx="1"/><rect x="100" y="75" width="4" height="3" rx="1"/><rect x="110" y="75" width="4" height="3" rx="1"/>
                    <rect x="90" y="85" width="4" height="3" rx="1"/><rect x="110" y="85" width="4" height="3" rx="1"/>
                    <rect x="225" y="65" width="4" height="3" rx="1"/><rect x="235" y="65" width="4" height="3" rx="1"/>
                    <rect x="225" y="75" width="4" height="3" rx="1"/><rect x="235" y="75" width="4" height="3" rx="1"/>
                    <rect x="360" y="80" width="4" height="3" rx="1"/><rect x="370" y="80" width="4" height="3" rx="1"/><rect x="380" y="80" width="4" height="3" rx="1"/>
                    <rect x="360" y="90" width="4" height="3" rx="1"/><rect x="380" y="90" width="4" height="3" rx="1"/>
                  </g>
                </svg>
                <!-- 餐厅：暖色氛围 -->
                <svg v-if="detailPoi.type === 'restaurant'" class="scenery-svg" viewBox="0 0 520 220" preserveAspectRatio="xMidYMax slice">
                  <circle cx="90" cy="70" r="55" fill="rgba(255,200,100,0.08)"/>
                  <circle cx="390" cy="100" r="70" fill="rgba(255,180,80,0.06)"/>
                  <circle cx="250" cy="50" r="40" fill="rgba(255,220,150,0.05)"/>
                  <circle cx="70" cy="170" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="0.8"/>
                  <circle cx="70" cy="170" r="28" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="0.8"/>
                  <circle cx="440" cy="150" r="55" fill="none" stroke="rgba(255,255,255,0.045)" stroke-width="0.8"/>
                  <circle cx="440" cy="150" r="32" fill="none" stroke="rgba(255,255,255,0.035)" stroke-width="0.8"/>
                  <circle cx="440" cy="150" r="14" fill="none" stroke="rgba(255,255,255,0.025)" stroke-width="0.8"/>
                  <circle cx="180" cy="120" r="20" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="0.8"/>
                  <circle cx="330" cy="70" r="18" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="0.8"/>
                  <path d="M0,110 Q130,50 260,90 Q390,45 520,80" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="1"/>
                  <path d="M0,145 Q140,95 270,130 Q400,90 520,120" fill="none" stroke="rgba(255,255,255,0.02)" stroke-width="0.8"/>
                </svg>
              </div>
              <div class="detail-hero-content">
                <img class="detail-hero-icon" :src="coverIconImage(detailPoi.type)" :alt="typeLabel(detailPoi.type)" />
                <h2 class="detail-hero-name">{{ detailPoi.name }}</h2>
                <span class="detail-hero-type">{{ typeLabel(detailPoi.type) }}</span>
              </div>
            </div>

            <!-- Info Body -->
            <div class="detail-body-scroll">
              <div class="detail-body-inner">
                <!-- Stats Row: Rating + Price + Popularity -->
                <div class="detail-stats">
                  <div class="detail-stat" v-if="detailPoi.rating">
                    <div class="stat-icon-wrap stat-icon-star">
                      <svg viewBox="0 0 20 20" fill="currentColor" width="22" height="22"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                    </div>
                    <div>
                      <span class="stat-value">{{ detailPoi.rating.toFixed(1) }}</span>
                      <span class="stat-label">评分</span>
                    </div>
                  </div>

                  <div class="detail-stat">
                    <div class="stat-icon-wrap stat-icon-coin">
                      <svg viewBox="0 0 20 20" fill="currentColor" width="22" height="22"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 000 2h4a1 1 0 110 2H7a1 1 0 100 2h4a3 3 0 002.683-4.133A3 3 0 0011 7H7a1 1 0 000 2h4a1 1 0 110 2H7z" clip-rule="evenodd"/></svg>
                    </div>
                    <div>
                      <span class="stat-value">{{ detailPoi.price > 0 ? `¥${detailPoi.price}` : '免费' }}</span>
                      <span class="stat-label">参考价格</span>
                    </div>
                  </div>

                  <div class="detail-stat" v-if="detailPoi.popularity_score">
                    <div class="stat-icon-wrap stat-icon-fire">
                      <svg viewBox="0 0 20 20" fill="currentColor" width="22" height="22"><path fill-rule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985 1.348-2.467-.363.59-.686 1.03-.903 1.47.27-.02.554-.05.847-.098.544-.09 1.17-.23 1.853-.507a1 1 0 00.604-1.264c-.52-1.643-1.65-2.637-2.487-3.318z" clip-rule="evenodd"/></svg>
                    </div>
                    <div>
                      <span class="stat-value">{{ (detailPoi.popularity_score / 10).toFixed(1) }}</span>
                      <span class="stat-label">热度</span>
                    </div>
                  </div>
                </div>

                <!-- Rating Stars (detailed) -->
                <div class="detail-stars-row" v-if="detailPoi.rating">
                  <div class="stars-visual">
                    <span v-for="i in 5" :key="i" class="star-icon" :class="{ filled: i <= Math.round(detailPoi.rating), half: i === Math.ceil(detailPoi.rating) && detailPoi.rating % 1 >= 0.25 && detailPoi.rating % 1 < 0.75 }">
                      <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                    </span>
                    <span class="stars-text">{{ detailPoi.rating.toFixed(1) }} 分</span>
                  </div>
                </div>

                <!-- Location -->
                <div class="detail-section" v-if="detailPoi.address || detailPoi.city">
                  <div class="section-header">
                    <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
                    <span>位置信息</span>
                  </div>
                  <p class="section-text">{{ detailPoi.address || '' }}{{ detailPoi.address && detailPoi.city ? '，' : '' }}{{ detailPoi.city || '' }}{{ detailPoi.district ? ' ' + detailPoi.district + '区' : '' }}</p>
                </div>

                <!-- Opening Hours -->
                <div class="detail-section" v-if="detailPoi.opening_hours">
                  <div class="section-header">
                    <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/></svg>
                    <span>开放时间</span>
                  </div>
                  <p class="section-text">{{ detailPoi.opening_hours }}</p>
                </div>

                <!-- Description -->
                <div class="detail-section" v-if="detailPoi.description">
                  <div class="section-header">
                    <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm3 1h6v1.5H7V5zm0 3h6v1.5H7V8zm0 3h4v1.5H7V11z" clip-rule="evenodd"/></svg>
                    <span>详细介绍</span>
                  </div>
                  <div class="section-desc-box">
                    <p>{{ detailPoi.description }}</p>
                  </div>
                </div>

                <!-- Tags -->
                <div class="detail-section" v-if="detailPoi.tags?.length">
                  <div class="section-header">
                    <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M17.707 9.293a1 1 0 010 1.414l-7 7a1 1 0 01-1.414 0l-7-7A.997.997 0 012 10V5a3 3 0 013-3h5c.256 0 .512.098.707.293l7 7zM5 6a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"/></svg>
                    <span>特色标签</span>
                  </div>
                  <div class="detail-tags-row">
                    <span v-for="t in detailPoi.tags" :key="t" class="detail-tag-chip">{{ t }}</span>
                  </div>
                </div>

                <!-- Reviews -->
                <div class="detail-section">
                  <div class="section-header">
                    <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"/></svg>
                    <span>用户评价</span>
                  </div>
                  <ReviewSection :poi-id="detailPoi.id" />
                </div>

                <!-- Action buttons -->
                <div class="detail-actions">
                  <button class="action-btn action-btn-primary">
                    <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/></svg>
                    加入行程
                  </button>
                  <button class="action-btn action-btn-secondary"
                    :class="{ 'favorited': detailPoi && favStore.isFavorite(detailPoi.id) }"
                    @click="detailPoi && favStore.toggleFavorite(detailPoi)">
                    <svg v-if="detailPoi && !favStore.isFavorite(detailPoi.id)" viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/></svg>
                    <svg v-else viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/></svg>
                    {{ detailPoi && favStore.isFavorite(detailPoi.id) ? '已收藏' : '收藏' }}
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
import { ref, computed } from 'vue'
import { useSearchStore } from '@/stores/search'
import { useFavoritesStore } from '@/stores/favorites'
import SearchBar from '@/components/search/SearchBar.vue'
import SearchFilters from '@/components/search/SearchFilters.vue'
import PoiCard from '@/components/search/PoiCard.vue'
import ReviewSection from '@/components/review/ReviewSection.vue'
import type { POIResult } from '@/types/search'

const store = useSearchStore()
const favStore = useFavoritesStore()
const filters = ref<Record<string, string>>({ city: '', poi_type: '' })
const lastKeyword = ref('')
const searched = ref(false)
const searchError = ref('')
const currentPage = ref(1)
const pageSize = 12
const detailVisible = ref(false)
const detailPoi = ref<POIResult | null>(null)
const quickSearches = ['故宫', '大熊猫', '迪士尼', '火锅', '长城']
const popularSearches = [
  { label: '故宫博物院', desc: '北京 · 世界遗产 · ¥60', keyword: '故宫', city: '北京', emoji: '🏯', image: '/assets/poi/gugong.png',
    poiData: { id: 'pop-1', name: '故宫博物院', type: 'attraction', city: '北京', district: '东城区', rating: 4.8, price: 60, tags: ['世界遗产', '博物馆', '明清皇家'], description: '故宫又名紫禁城，是中国明清两代的皇家宫殿，也是世界上现存规模最大、保存最为完整的木质结构古建筑之一。占地面积约72万平方米，建筑面积约15万平方米，有大小宫殿七十多座，房屋九千余间。', address: '北京市东城区景山前街4号', opening_hours: '08:30 - 17:00（周一闭馆）', popularity_score: 980, lat: 39.9163, lng: 116.3972 } },
  { label: '成都大熊猫基地', desc: '成都 · 亲子必去 · ¥55', keyword: '大熊猫', city: '成都', emoji: '🐼', image: '/assets/poi/panda.png',
    poiData: { id: 'pop-2', name: '成都大熊猫繁育研究基地', type: 'attraction', city: '成都', district: '成华区', rating: 4.7, price: 55, tags: ['亲子游', '大熊猫', '自然生态'], description: '成都大熊猫繁育研究基地是世界著名的大熊猫迁地保护基地、科研繁育基地、公众教育基地和教育旅游基地。基地内常年饲养着约100只大熊猫。', address: '四川省成都市成华区外北三环熊猫大道1375号', opening_hours: '07:30 - 18:00', popularity_score: 920, lat: 30.7367, lng: 104.1451 } },
  { label: '上海迪士尼', desc: '上海 · 主题乐园 · ¥499', keyword: '迪士尼', city: '上海', emoji: '🏰', image: '/assets/poi/disney.png',
    poiData: { id: 'pop-3', name: '上海迪士尼乐园', type: 'attraction', city: '上海', district: '浦东新区', rating: 4.6, price: 499, tags: ['主题乐园', '亲子游', '梦幻世界'], description: '上海迪士尼乐园是中国内地首座迪士尼主题乐园，拥有米奇大街、奇想花园、探险岛、宝藏湾、明日世界、梦幻世界和玩具总动员七大主题园区。', address: '上海市浦东新区川沙镇黄赵路310号', opening_hours: '09:00 - 20:00（以当日为准）', popularity_score: 950, lat: 31.1434, lng: 121.6580 } },
  { label: '西安兵马俑', desc: '西安 · 世界奇迹 · ¥120', keyword: '兵马俑', city: '西安', emoji: '🗿', image: '/assets/poi/bingmayong.png',
    poiData: { id: 'pop-4', name: '秦始皇兵马俑博物馆', type: 'attraction', city: '西安', district: '临潼区', rating: 4.9, price: 120, tags: ['世界遗产', '历史文化', '秦朝'], description: '秦始皇陵兵马俑被誉为"世界第八大奇迹"，是秦始皇陵园中一组大型陪葬陶塑。三个坑共出土约8000件真人大小陶俑、陶马及大量青铜兵器。', address: '陕西省西安市临潼区秦陵北路', opening_hours: '08:30 - 17:00', popularity_score: 960, lat: 34.3847, lng: 109.2783 } },
  { label: '外滩夜景', desc: '上海 · 免费 · 城市地标', keyword: '外滩', city: '上海', emoji: '🌃', image: '/assets/poi/waitan.png',
    poiData: { id: 'pop-5', name: '外滩', type: 'attraction', city: '上海', district: '黄浦区', rating: 4.7, price: 0, tags: ['城市地标', '夜景免费', '万国建筑'], description: '外滩位于上海市中心区的黄浦江畔，是上海最具标志性的景点之一。全长1.5公里，南起延安东路，北至苏州河上的外白渡桥，东面即黄浦江，西面是旧上海金融、外贸机构的集中地。', address: '上海市黄浦区中山东一路', opening_hours: '全天开放', popularity_score: 890, lat: 31.2397, lng: 121.4900 } },
  { label: '宽窄巷子', desc: '成都 · 免费 · 美食街区', keyword: '宽窄巷子', city: '成都', emoji: '🏘️', image: '/assets/poi/kuanzhai.png',
    poiData: { id: 'pop-6', name: '宽窄巷子', type: 'attraction', city: '成都', district: '青羊区', rating: 4.5, price: 0, tags: ['美食街区', '老成都', '免费游览'], description: '宽窄巷子由宽巷子、窄巷子和井巷子三条平行排列的老式街道及其之间的四合院群落组成，是成都市三大历史文化保护区之一，集中了清末民初的建筑风格。', address: '四川省成都市青羊区金河路口宽窄巷子', opening_hours: '全天开放', popularity_score: 850, lat: 30.6719, lng: 104.0566 } },
  { label: '北京烤鸭', desc: '北京 · 美食 · ¥150', keyword: '烤鸭', city: '北京', emoji: '🦆', image: '/assets/poi/kaoya.png',
    poiData: { id: 'pop-7', name: '全聚德烤鸭店', type: 'restaurant', city: '北京', district: '东城区', rating: 4.4, price: 150, tags: ['北京烤鸭', '百年老字号', '京菜'], description: '全聚德创建于1864年，是享誉中外的中华老字号餐厅，以其挂炉烤鸭闻名于世。烤鸭色泽红润、肉质细嫩、味道醇厚，被誉为"天下第一鸭"。', address: '北京市东城区前门大街30号', opening_hours: '10:30 - 21:00', popularity_score: 820, lat: 39.9000, lng: 116.3970 } },
  { label: '成都火锅', desc: '成都 · 川菜 · ¥120', keyword: '火锅', city: '成都', emoji: '🍲', image: '/assets/poi/huoguo.png',
    poiData: { id: 'pop-8', name: '蜀大侠火锅', type: 'restaurant', city: '成都', district: '武侯区', rating: 4.6, price: 120, tags: ['四川火锅', '麻辣鲜香', '川菜'], description: '蜀大侠火锅源于成都，将传统川味火锅与武侠文化相结合，环境古朴典雅，锅底麻辣鲜香、回味悠长，是体验正宗成都火锅文化的绝佳选择。', address: '四川省成都市武侯区春熙路商圈', opening_hours: '11:00 - 次日02:00', popularity_score: 870, lat: 30.6526, lng: 104.0745 } },
]

const typeLabel = (t: string) => ({ attraction: '景点', hotel: '酒店', restaurant: '餐厅' } as Record<string, string>)[t] || t
const coverGradient = (t: string) => ({ attraction: 'linear-gradient(160deg, #0A4F5C 0%, #0D7377 30%, #14919B 60%, #0D7377 100%)', hotel: 'linear-gradient(160deg, #1A0533 0%, #2D1B4E 30%, #4A2066 60%, #2D1B4E 100%)', restaurant: 'linear-gradient(160deg, #3D1C00 0%, #6B2F00 30%, #8B4513 60%, #5C2800 100%)' } as Record<string, string>)[t] || 'linear-gradient(160deg, #1a1a2e, #16213e, #0f3460)'
const coverEmoji = (t: string) => ({ attraction: '🏛️', hotel: '🏨', restaurant: '🍽️' } as Record<string, string>)[t] || '📍'
const coverIconImage = (t: string) => ({ attraction: '/assets/poi/type_attraction.png', hotel: '/assets/poi/type_hotel.png', restaurant: '/assets/poi/type_restaurant.png' } as Record<string, string>)[t] || '/assets/poi/type_attraction.png'

function onFilterChange() { if (searched.value && lastKeyword.value) doSearch(lastKeyword.value) }

async function doSearch(keyword: string) {
  searchError.value = ''
  store.loading = true
  try {
    await store.search({ keyword, city: filters.value.city || undefined, poi_type: filters.value.poi_type || undefined, page: currentPage.value, page_size: pageSize })
  } catch (err: any) {
    searchError.value = err?.response?.data?.detail || err?.message || '搜索服务连接失败'
  } finally { store.loading = false }
}

async function handleSearch(keyword: string) { lastKeyword.value = keyword; searched.value = true; currentPage.value = 1; await doSearch(keyword) }
async function handleQuickSearch(keyword: string, city?: string) { if (city) filters.value.city = city; await handleSearch(keyword) }
async function handlePageChange(page: number) { currentPage.value = page; await doSearch(lastKeyword.value) }
async function retrySearch() { await doSearch(lastKeyword.value) }
function showPoiDetail(poi: POIResult) { detailPoi.value = poi; detailVisible.value = true }
</script>

<style scoped lang="scss">
$bg-warm: #FAF8F3;
$bg-white: #FFFFFF;
$bg-oat: #F5F0E8;
$brand-brown: #A68B7A;
$brand-sage: #B8C4B8;
$text-primary: #3D3D3D;
$text-secondary: #6B6B6B;
$text-muted: #B8B0A8;
$border: #E8D5D0;

.search-view { padding-bottom: var(--space-4xl); background: $bg-warm; min-height: 100vh; }

.search-hero {
  position: relative; overflow: hidden;
  padding: var(--space-3xl) var(--space-lg) var(--space-2xl);
  text-align: center;
  background: linear-gradient(180deg, $bg-white 0%, $bg-warm 100%);
  border-bottom: 1px solid $border;
}

.search-hero-bg { position: absolute; inset: 0; }
.hero-orb { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.06;
  &.orb-a { width: 400px; height: 400px; background: #f59e0b; top: -100px; right: -100px; }
  &.orb-b { width: 350px; height: 350px; background: #3b82f6; bottom: -100px; left: -100px; }
}

.search-hero-content { position: relative; z-index: 1; }

.search-title { font-size: 32px; font-weight: 800; color: $text-primary; margin-bottom: 8px; }
.search-subtitle { font-size: 15px; color: $text-muted; margin-bottom: var(--space-xl); }

.search-body { max-width: 1200px; margin: 0 auto; padding: var(--space-xl) var(--space-lg); }

.results-stats {
  display: flex; justify-content: space-between; align-items: center;
  padding: 14px 0; margin-bottom: 20px;
  font-size: 14px; color: $text-secondary;
  strong { color: $text-primary; }
  .stats-count { color: $brand-brown; font-weight: 600; }
}

.results-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }

.skeleton-card {
  background: $bg-oat; border-radius: 16px; border: 1px solid $border; overflow: hidden; height: 280px;
  .sk-cover { height: 120px; }
  .sk-body { padding: 16px; }
  .sk-title { height: 20px; width: 60%; border-radius: 6px; margin-bottom: 10px; }
  .sk-meta { height: 14px; width: 80%; border-radius: 6px; margin-bottom: 14px; }
  .sk-tags { display: flex; gap: 8px; }
  .sk-tag { height: 24px; width: 60px; border-radius: 12px; }
}

.error-state {
  text-align: center; padding: 80px 20px; color: $text-secondary;
  svg { color: $brand-brown; margin-bottom: 16px; }
  h3 { font-size: 18px; color: $text-primary; margin-bottom: 8px; }
  p { margin-bottom: 20px; max-width: 400px; margin-left: auto; margin-right: auto; }
}

.retry-btn {
  padding: 10px 28px; border: none; border-radius: 12px;
  background: linear-gradient(135deg, #fbbf24, #f59e0b); color: #0f172a;
  font-size: 14px; font-weight: 600; cursor: pointer; font-family: inherit;
  box-shadow: 0 4px 16px rgba(245,158,11,0.25);
  &:hover { box-shadow: 0 6px 24px rgba(245,158,11,0.35); transform: translateY(-1px); }
}

.empty-state {
  text-align: center; padding: 80px 20px; color: $text-secondary;
  svg { color: $border; margin-bottom: 16px; }
  h3 { font-size: 18px; color: $text-primary; margin-bottom: 8px; }
  p { margin-bottom: 20px; }
}

.quick-searches { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }
.quick-chip {
  padding: 8px 18px; border: 1px solid $border; border-radius: 20px;
  background: $bg-oat; color: $text-secondary; font-size: 13px;
  cursor: pointer; font-family: inherit;
  transition: all 0.25s;
  &:hover { border-color: $brand-brown; color: $brand-brown; }
}

.welcome-state { padding: var(--space-xl) 0; }
.welcome-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }
.welcome-chip {
  display: flex; flex-direction: column; align-items: center; gap: 10px;
  padding: 28px 20px; background: $bg-oat; border: 1px solid $border;
  border-radius: 16px; cursor: pointer; transition: all 0.3s ease;
  &:hover { border-color: $brand-brown; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
}
.chip-image-wrap {
  width: 80px; height: 80px; border-radius: 14px;
  overflow: hidden; margin-bottom: 4px;
}
.chip-image {
  width: 100%; height: 100%; object-fit: cover;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.welcome-chip:hover .chip-image { transform: scale(1.08); }
.chip-label { font-size: 15px; font-weight: 600; color: $text-primary; }
.chip-desc { font-size: 12px; color: $text-muted; }

.pagination { display: flex; justify-content: center; margin-top: var(--space-2xl); }

// === Fullscreen Detail Panel (Centered Modal) ===
.detail-overlay {
  position: fixed; inset: 0; z-index: 2000;
  background: rgba(61,61,61,0.45); backdrop-filter: blur(6px);
  display: flex; align-items: center; justify-content: center;
  -webkit-overflow-scrolling: touch;
}
.detail-panel {
  width: 680px; max-width: 92vw; height: 85vh; max-height: 820px;
  background: $bg-white; display: flex; flex-direction: column;
  overflow: hidden; border-radius: 22px;
  box-shadow: 0 24px 72px rgba(0,0,0,0.2), 0 4px 16px rgba(0,0,0,0.08);
  position: relative;
}
.detail-close {
  position: absolute; top: 16px; right: 18px; z-index: 10;
  width: 36px; height: 36px; border-radius: 50%; border: none;
  background: rgba(0,0,0,0.3); color: #fff;
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

// Scrollable body
.detail-body-scroll { flex: 1; overflow-y: auto; -webkit-overflow-scrolling: touch; }
.detail-body-inner { padding: 24px 28px 40px; }

// Stats cards row
.detail-stats {
  display: flex; gap: 12px; margin-bottom: 20px;
}
.detail-stat {
  flex: 1; display: flex; align-items: center; gap: 12px;
  padding: 16px; background: $bg-oat; border-radius: 14px;
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

// Stars row
.detail-stars-row { margin-bottom: 20px; }
.stars-visual {
  display: flex; align-items: center; gap: 3px;
}
.star-icon { color: $border; display: flex; &.filled { color: #f59e0b; } &.half { color: #f59e0b; opacity: 0.5; } }
.stars-text { font-size: 13px; font-weight: 600; color: $brand-brown; margin-left: 8px; }

// Info sections
.detail-section {
  margin-bottom: 20px;
}
.section-header {
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 10px; color: $brand-brown; font-size: 13px; font-weight: 600;
}
.section-text { font-size: 14px; color: $text-secondary; line-height: 1.7; margin: 0; }

.section-desc-box {
  padding: 16px; border-radius: 12px;
  background: $bg-oat; border: 1px solid $border;
  p { margin: 0; font-size: 14px; color: $text-secondary; line-height: 1.85; }
}

// Tags row
.detail-tags-row { display: flex; flex-wrap: wrap; gap: 8px; }
.detail-tag-chip {
  padding: 6px 14px; border-radius: 20px;
  font-size: 12px; font-weight: 500; color: $brand-brown;
  background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.15);
}

// Action buttons
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
  background: $bg-oat; color: $text-secondary; border: 1px solid $border;
  &:hover { color: $brand-brown; border-color: rgba(245,158,11,0.3); }
  &.favorited {
    color: #ef4444; border-color: rgba(239,68,68,0.25); background: rgba(239,68,68,0.08);
    &:hover { color: #f87171; border-color: rgba(239,68,68,0.4); background: rgba(239,68,68,0.12); }
  }
}

// Panel animation (centered fade+scale)
.panel-slide-enter-active { transition: opacity 0.3s ease, transform 0.32s cubic-bezier(0.16, 1, 0.3, 1); }
.panel-slide-leave-active { transition: opacity 0.2s ease, transform 0.22s cubic-bezier(0.4, 0, 0.2, 1); }
.panel-slide-enter-from { opacity: 0; .detail-panel { transform: translateY(20px) scale(0.96); } }
.panel-slide-leave-to { opacity: 0; .detail-panel { transform: translateY(-8px) scale(0.97); } }

@media (max-width: 540px) {
  .detail-panel { width: 96vw; height: 92vh; max-height: none; border-radius: 18px; }
  .detail-hero { padding: 48px 20px 28px; min-height: 170px; }
  .detail-body-inner { padding: 20px; }
  .detail-stats { flex-direction: column; gap: 8px; }
}

// === Dark theme el-pagination fine-tuning ===
:deep(.el-pagination) {
  .el-pager li {
    background: $bg-oat; border-radius: 8px;
    color: $text-secondary; font-weight: 500;
    min-width: 34px; height: 34px; line-height: 34px;
    &:hover { color: $brand-brown; }
    &.is-active {
      background: linear-gradient(135deg, #fbbf24, #f59e0b);
      color: #0f172a; font-weight: 700;
    }
  }
  button {
    background: $bg-oat; border-radius: 8px;
    color: $text-secondary; height: 34px;
    &:hover { color: $brand-brown; }
    &:disabled { color: $text-muted; opacity: 0.4; }
  }
}

@media (max-width: 768px) {
  .results-grid { grid-template-columns: 1fr; }
  .welcome-grid { grid-template-columns: repeat(2, 1fr); }
  .results-stats { flex-direction: column; align-items: flex-start; gap: 4px; }
}
</style>
