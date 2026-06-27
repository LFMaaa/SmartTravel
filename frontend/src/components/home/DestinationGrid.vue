<template>
  <section class="destination-section">
    <div class="container">
      <SectionTitle overline="热门目的地" subtitle="精选最受欢迎的旅行目的地，点击即可开始 AI 规划" centered>
        探索精彩目的地
      </SectionTitle>

      <Swiper
        :modules="modules"
        :slides-per-view="'auto'"
        :space-between="20"
        :centered-slides="false"
        :loop="true"
        :autoplay="{ delay: 3000, disableOnInteraction: false }"
        :pagination="{ clickable: true }"
        :breakpoints="{ 320: { slidesPerView: 1.2, spaceBetween: 12 }, 640: { slidesPerView: 2, spaceBetween: 16 }, 1024: { slidesPerView: 3, spaceBetween: 20 }, 1280: { slidesPerView: 4, spaceBetween: 20 } }"
        class="destination-swiper"
      >
        <SwiperSlide v-for="dest in destinations" :key="dest.id">
          <div class="dest-card" @click="goGenerate(dest.query)">
            <div class="dest-cover" :style="{ background: dest.gradient }">
              <img class="dest-image" :src="dest.image" :alt="dest.name" loading="lazy" />
              <div class="dest-overlay">
                <span class="dest-name">{{ dest.name }}</span>
              </div>
              <div class="dest-shine"></div>
            </div>
            <div class="dest-info">
              <h4>{{ dest.title }}</h4>
              <div class="dest-tags">
                <span v-for="tag in dest.tags" :key="tag" class="dest-tag">{{ tag }}</span>
              </div>
              <p class="dest-desc">{{ dest.desc }}</p>
            </div>
          </div>
        </SwiperSlide>
      </Swiper>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'
import SectionTitle from '@/components/common/SectionTitle.vue'

const router = useRouter()
const modules = [Autoplay, Pagination]

const destinations = [
  { id: 1, name: '北京', emoji: '🏯', image: '/assets/destinations/beijing.png', gradient: 'linear-gradient(135deg, #E17055, #F7A800)', title: '北京4日文化深度游', tags: ['历史文化', '美食', '亲子'], desc: '故宫、长城、颐和园，感受千年古都魅力', query: '我想带家人去北京玩4天，喜欢历史文化，预算1万' },
  { id: 2, name: '成都', emoji: '🐼', image: '/assets/destinations/chengdu.png', gradient: 'linear-gradient(135deg, #00B894, #0D7377)', title: '成都3日美食休闲游', tags: ['美食', '休闲', '自然'], desc: '火锅、大熊猫、宽窄巷子，慢生活天堂', query: '和朋友去成都吃美食看大熊猫，3天时间' },
  { id: 3, name: '上海', emoji: '🌃', image: '/assets/destinations/shanghai.png', gradient: 'linear-gradient(135deg, #6C5CE7, #74B9FF)', title: '上海3日都市时尚游', tags: ['都市', '购物', '亲子'], desc: '外滩、迪士尼、新天地，摩登都市体验', query: '带小朋友去上海迪士尼和外滩，3天时间' },
  { id: 4, name: '云南', emoji: '🏔️', image: '/assets/destinations/yunnan.png', gradient: 'linear-gradient(135deg, #FF6B35, #E17055)', title: '云南6日自然之旅', tags: ['自然风光', '摄影', '休闲'], desc: '大理洱海、丽江古城、玉龙雪山', query: '一个人去云南发呆拍照，6天时间，预算8000' },
  { id: 5, name: '三亚', emoji: '🏖️', image: '/assets/destinations/sanya.png', gradient: 'linear-gradient(135deg, #0984E3, #00CEC9)', title: '三亚5日蜜月度假', tags: ['海岛', '度假', '蜜月'], desc: '阳光沙滩、海鲜大餐、水上运动', query: '蜜月去三亚，5天，预算2万，要浪漫' },
  { id: 6, name: '西安', emoji: '🏛️', image: '/assets/destinations/xian.png', gradient: 'linear-gradient(135deg, #D63031, #E17055)', title: '西安3日历史探秘', tags: ['历史文化', '美食', '古迹'], desc: '兵马俑、古城墙、回民街美食', query: '去西安看兵马俑吃小吃，3天，预算5000' },
]

function goGenerate(query: string) { router.push({ name: 'itinerary-generate', query: { q: query } }) }
</script>

<style scoped lang="scss">
$bg-card: #111827;
$bg-elevated: #1a2235;
$brand-amber: #f59e0b;
$text-primary: #f1f5f9;
$text-secondary: #94a3b8;
$text-muted: #64748b;
$border: #1e293b;

.destination-section {
  padding: var(--space-4xl) 0;
  background: $bg-card;
}

.container { max-width: 1200px; margin: 0 auto; padding: 0 var(--space-lg); }

.destination-swiper { padding: 8px 4px 48px; }

.dest-card {
  background: $bg-elevated;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid $border;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);

  &:hover {
    transform: translateY(-6px);
    border-color: rgba(245, 158, 11, 0.3);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(245, 158, 11, 0.1);

    .dest-image { transform: scale(1.08); }
    .dest-shine { opacity: 0.15; }
  }
}

.dest-cover {
  height: 170px;
  display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden;
}

.dest-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative; z-index: 0;
}

.dest-overlay {
  position: absolute; bottom: 0; left: 0; right: 0;
  padding: 14px 18px;
  background: linear-gradient(transparent, rgba(0,0,0,0.6));
  z-index: 1;
  .dest-name { color: #fff; font-size: 16px; font-weight: 700; }
}

.dest-shine {
  position: absolute; inset: 0;
  background: radial-gradient(circle at 30% 20%, rgba(255,255,255,0.2), transparent);
  opacity: 0; transition: opacity 0.35s ease;
  pointer-events: none;
}

.dest-info {
  padding: 18px;
  h4 { font-size: 15px; font-weight: 600; color: $text-primary; margin-bottom: 10px; }
}

.dest-tags { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px; }

.dest-tag {
  padding: 3px 10px; border-radius: var(--radius-full);
  font-size: 11px; font-weight: 500;
  background: rgba(245, 158, 11, 0.08);
  color: $brand-amber;
  border: 1px solid rgba(245, 158, 11, 0.12);
}

.dest-desc {
  font-size: 13px; color: $text-muted; line-height: 1.5;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}

:deep(.swiper-pagination-bullet) { background: $text-muted; opacity: 0.4; }
:deep(.swiper-pagination-bullet-active) { background: $brand-amber; opacity: 1; }
</style>
