<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-bg-orb orb-left"></div>
      <div class="hero-bg-orb orb-right"></div>
      <div class="hero-container">
        <div class="hero-badge">✨ AI 驱动的智能旅行体验</div>
        <h1 class="hero-title">
          让每一次旅行<br>
          都成为<span>难忘的故事</span>
        </h1>
        <p class="hero-subtitle">只需描述你的梦想旅程，AI 为你定制专属行程</p>

        <!-- AI Chat Input -->
        <div class="hero-chat-box">
          <input
            v-model="chatInput"
            type="text"
            class="chat-input"
            placeholder="告诉我你想去哪里，想要什么体验..."
            @keyup.enter="sendMessage"
          />
          <button class="chat-send-btn" @click="sendMessage">➤</button>
        </div>

        <!-- Quick Tags -->
        <div class="hero-tags">
          <span
            v-for="tag in quickTags"
            :key="tag"
            class="tag-item"
            @click="selectTag(tag)"
          >{{ tag }}</span>
        </div>
      </div>
    </section>

    <!-- Popular Destinations -->
    <section class="destinations">
      <div class="section-container">
        <div class="section-header">
          <div class="section-label">Popular Destinations</div>
          <h2 class="section-title">热门<span>目的地</span></h2>
        </div>
        <div class="destinations-grid">
          <div
            v-for="dest in destinations"
            :key="dest.name"
            class="dest-card"
            @click="exploreDestination(dest.name)"
          >
            <div class="dest-image-wrapper">
              <img :src="dest.image" :alt="dest.name" class="dest-image" />
              <div class="dest-overlay"></div>
            </div>
            <div class="dest-info">
              <h3 class="dest-name">{{ dest.name }}</h3>
              <p class="dest-desc">{{ dest.desc }}</p>
              <span class="dest-tag">{{ dest.tag }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- AI Recommendations -->
    <section class="ai-recommendations">
      <div class="section-container">
        <div class="section-header">
          <div class="section-label">AI Recommendations</div>
          <h2 class="section-title">AI 精选<span>行程</span></h2>
        </div>
        <div class="rec-grid">
          <div
            v-for="rec in recommendations"
            :key="rec.title"
            class="rec-card"
            @click="viewItinerary(rec.title)"
          >
            <div class="rec-header">
              <div class="rec-icon">{{ rec.icon }}</div>
              <div>
                <h3 class="rec-title">{{ rec.title }}</h3>
                <p class="rec-subtitle">{{ rec.subtitle }}</p>
              </div>
            </div>
            <div class="rec-content">
              <div v-for="(item, idx) in rec.items" :key="idx" class="rec-item">
                <span class="rec-dot"></span>
                <span class="rec-text">{{ item }}</span>
              </div>
            </div>
            <button class="rec-btn">查看详情 →</button>
          </div>
        </div>
      </div>
    </section>

    <!-- Feature Showcase -->
    <section class="features">
      <div class="section-container">
        <div class="section-header">
          <div class="section-label">Why Choose Us</div>
          <h2 class="section-title">为什么选择<span>我们</span></h2>
        </div>
        <div class="features-grid">
          <div v-for="feat in features" :key="feat.title" class="feature-card">
            <div class="feature-icon">{{ feat.icon }}</div>
            <h3>{{ feat.title }}</h3>
            <p>{{ feat.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-container">
        <div class="footer-content">
          <div class="footer-brand">
            <div class="footer-logo">
              <span class="footer-logo-icon">🌿</span>
              <span class="footer-logo-text">旅游AI</span>
            </div>
            <p class="footer-desc">用AI重新定义旅行，为每一位探索者打造独一无二的旅程体验。从灵感激发到行程落地，我们陪伴每一步。</p>
          </div>
          <div class="footer-column">
            <h4>产品服务</h4>
            <ul>
              <li><a href="#">AI行程规划</a></li>
              <li><a href="#">智能酒店推荐</a></li>
              <li><a href="#">当地体验预订</a></li>
              <li><a href="#">旅行保险</a></li>
            </ul>
          </div>
          <div class="footer-column">
            <h4>关于我们</h4>
            <ul>
              <li><a href="#">品牌故事</a></li>
              <li><a href="#">加入团队</a></li>
              <li><a href="#">合作伙伴</a></li>
              <li><a href="#">联系我们</a></li>
            </ul>
          </div>
          <div class="footer-column">
            <h4>帮助中心</h4>
            <ul>
              <li><a href="#">使用指南</a></li>
              <li><a href="#">常见问题</a></li>
              <li><a href="#">退改政策</a></li>
              <li><a href="#">隐私条款</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <p>© 2026 旅游AI. 让旅行更自然，更美好。</p>
          <div class="footer-social">
            <span>📷</span>
            <span>🐦</span>
            <span>💬</span>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const chatInput = ref('')

const quickTags = [
  '🏔️ 国内小众秘境',
  '🏝️ 海岛度假',
  '🎋 古镇慢生活',
  '👨‍👩‍👧 亲子游推荐',
  '🍜 美食之旅',
]

const destinations = ref([
  {
    name: '云南大理',
    desc: '苍山洱海间的诗意栖居',
    tag: '慢生活',
    image: 'https://picsum.photos/seed/dali/400/300',
  },
  {
    name: '浙江莫干山',
    desc: '竹海深处的民宿天堂',
    tag: '自然度假',
    image: 'https://picsum.photos/seed/moganshan/400/300',
  },
  {
    name: '福建霞浦',
    desc: '光影交织的滩涂画卷',
    tag: '摄影圣地',
    image: 'https://picsum.photos/seed/xiapu/400/300',
  },
  {
    name: '新疆喀纳斯',
    desc: '神的后花园，秋色童话',
    tag: '自然风光',
    image: 'https://picsum.photos/seed/kanas/400/300',
  },
])

const recommendations = ref([
  {
    icon: '🏔️',
    title: '川西小环线7日',
    subtitle: '雪山、草原、藏寨',
    items: ['成都 → 四姑娘山 → 丹巴', '墨石公园 → 塔公草原', '新都桥 → 康定 → 成都'],
  },
  {
    icon: '🌊',
    title: '闽南海岸线5日',
    subtitle: '海岛、古镇、美食',
    items: ['厦门鼓浪屿深度游', '泉州古城文化探索', '漳州土楼群探访'],
  },
  {
    icon: '🍂',
    title: '东北秋色6日',
    subtitle: '红叶、温泉、民俗',
    items: ['长白山天池观秋', '延边朝鲜族风情', '本溪红叶谷徒步'],
  },
])

const features = [
  { icon: '🤖', title: 'AI 智能规划', desc: '基于Dify大模型，智能解析你的旅行意图，生成个性化行程方案' },
  { icon: '⚡', title: '实时流式生成', desc: '毫秒级响应，边聊边生成，所见即所得的极致体验' },
  { icon: '🔄', title: '动态重排', desc: '遇到天气变化或突发事件，AI自动重排行程，保障旅行顺利进行' },
  { icon: '💳', title: '一站式预订', desc: '集成支付宝沙箱支付，酒店、门票、餐饮一键预订' },
  { icon: '📱', title: '短信验证登录', desc: '手机号+短信验证码快速登录注册，安全便捷' },
  { icon: '🔍', title: '智能搜索', desc: 'Elasticsearch全文搜索，快速找到心仪的目的地和POI' },
]

function sendMessage() {
  if (chatInput.value.trim()) {
    router.push({ path: '/itinerary/generate', query: { q: chatInput.value.trim() } })
  }
}

function selectTag(tag: string) {
  chatInput.value = tag.replace(/^[^\s]+\s/, '')
  router.push({ path: '/itinerary/generate', query: { q: chatInput.value } })
}

function exploreDestination(name: string) {
  router.push({ path: '/search', query: { q: name } })
}

function viewItinerary(title: string) {
  router.push({ path: '/itinerary/generate', query: { q: title } })
}
</script>

<style scoped lang="scss">
// ============================================
// Earth & Elegance — Design Tokens
// ============================================
$bg-warm: #FAF8F3;
$bg-oat: #F5F0E8;
$bg-cream: #FDFBF7;
$bg-white: #FFFFFF;
$brand-brown: #A68B7A;
$brand-brown-light: #C4A89A;
$brand-nude: #E8D5D0;
$brand-sage: #B8C4B8;
$brand-sage-dark: #9AAA9A;
$text-primary: #3D3D3D;
$text-secondary: #6B6B6B;
$text-muted: #B8B0A8;
$border: #E8D5D0;
$border-light: rgba(166, 139, 122, 0.08);

// ============================================
// Hero
// ============================================
.hero {
  background: linear-gradient(180deg, $bg-cream 0%, $bg-warm 100%);
  padding: 100px 0 120px;
  text-align: center;
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid rgba(232, 213, 208, 0.3);
}

.hero-bg-orb {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(120px);
  opacity: 0.08;

  &.orb-left {
    width: 500px; height: 500px;
    background: rgba(184, 196, 184, 0.3);
    top: -30%; left: -10%;
  }
  &.orb-right {
    width: 400px; height: 400px;
    background: rgba(232, 213, 208, 0.35);
    bottom: -20%; right: -5%;
  }
}

.hero-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 40px;
  position: relative;
  z-index: 1;
}

.hero-badge {
  display: inline-block;
  background: rgba(184, 196, 184, 0.2);
  color: $brand-brown;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 30px;
  letter-spacing: 1px;
}

.hero-title {
  font-size: 52px;
  font-weight: 300;
  color: $text-primary;
  margin-bottom: 20px;
  line-height: 1.3;

  span {
    font-weight: 600;
    color: $brand-brown;
  }
}

.hero-subtitle {
  font-size: 18px;
  color: $text-secondary;
  margin-bottom: 50px;
  font-weight: 300;
}

// Chat Input
.hero-chat-box {
  background: $bg-white;
  border-radius: 24px;
  padding: 8px;
  box-shadow: 0 8px 40px rgba(166, 139, 122, 0.12);
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 30px;
  border: 1px solid rgba(232, 213, 208, 0.5);
}

.chat-input {
  flex: 1;
  border: none;
  padding: 16px 20px;
  font-size: 16px;
  font-family: inherit;
  background: transparent;
  outline: none;
  color: $text-primary;

  &::placeholder {
    color: $text-muted;
  }
}

.chat-send-btn {
  background: $brand-sage;
  border: none;
  width: 50px; height: 50px;
  border-radius: 50%;
  color: white;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  &:hover {
    background: $brand-brown;
    box-shadow: 0 4px 16px rgba(166, 139, 122, 0.25);
    transform: scale(1.05);
  }
}

// Tags
.hero-tags {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.tag-item {
  background: rgba(232, 213, 208, 0.3);
  border: 1px solid $brand-nude;
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 14px;
  color: $brand-brown;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: $brand-nude;
    color: white;
    transform: translateY(-2px);
  }
}

// ============================================
// Common Section Styles
// ============================================
.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-label {
  font-size: 12px;
  color: $brand-sage;
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-bottom: 12px;
  font-weight: 500;
}

.section-title {
  font-size: 36px;
  font-weight: 300;
  color: $text-primary;

  span {
    font-weight: 600;
    color: $brand-brown;
  }
}

// ============================================
// Destinations
// ============================================
.destinations {
  padding: 100px 0;
  background: $bg-oat;
}

.destinations-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.dest-card {
  background: $bg-white;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid $brand-nude;
  transition: all 0.4s ease;
  cursor: pointer;

  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(166, 139, 122, 0.15);
    border-color: $brand-sage;

    .dest-image { transform: scale(1.05); }
  }
}

.dest-image-wrapper {
  width: 100%;
  height: 200px;
  overflow: hidden;
  position: relative;
}

.dest-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.dest-overlay {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 60px;
  background: linear-gradient(transparent, rgba(0,0,0,0.3));
  pointer-events: none;
}

.dest-info {
  padding: 20px;
}

.dest-name {
  font-size: 18px;
  font-weight: 500;
  color: $text-primary;
  margin-bottom: 6px;
}

.dest-desc {
  font-size: 13px;
  color: $text-secondary;
  margin-bottom: 12px;
}

.dest-tag {
  display: inline-block;
  background: rgba(184, 196, 184, 0.2);
  color: $brand-brown;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
}

// ============================================
// AI Recommendations
// ============================================
.ai-recommendations {
  padding: 100px 0;
  background: $bg-warm;
}

.rec-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.rec-card {
  background: $bg-white;
  border-radius: 24px;
  padding: 30px;
  border: 1px solid $brand-sage;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
  cursor: pointer;

  &::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, $brand-nude 0%, $brand-sage 100%);
  }

  &:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(166, 139, 122, 0.1);
  }
}

.rec-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.rec-icon {
  width: 48px; height: 48px;
  background: linear-gradient(135deg, $brand-nude 0%, $brand-sage 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.rec-title {
  font-size: 18px;
  font-weight: 500;
  color: $text-primary;
}

.rec-subtitle {
  font-size: 13px;
  color: $text-secondary;
}

.rec-content {
  margin-bottom: 20px;
}

.rec-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px dashed $border;

  &:last-child { border-bottom: none; }
}

.rec-dot {
  width: 8px; height: 8px;
  background: $brand-sage;
  border-radius: 50%;
  flex-shrink: 0;
}

.rec-text {
  font-size: 14px;
  color: $text-secondary;
}

.rec-btn {
  width: 100%;
  padding: 14px;
  background: transparent;
  border: 1.5px solid $brand-nude;
  border-radius: 12px;
  color: $brand-brown;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;

  &:hover {
    background: $brand-nude;
    color: white;
  }
}

// ============================================
// Features
// ============================================
.features {
  padding: 100px 0;
  background: $bg-oat;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.feature-card {
  background: $bg-white;
  border-radius: 20px;
  padding: 32px 28px;
  text-align: center;
  border: 1px solid $brand-nude;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(166, 139, 122, 0.08);
    border-color: $brand-sage;
  }

  .feature-icon {
    font-size: 40px;
    margin-bottom: 16px;
  }

  h3 {
    font-size: 18px;
    font-weight: 500;
    color: $text-primary;
    margin-bottom: 10px;
  }

  p {
    font-size: 14px;
    color: $text-secondary;
    line-height: 1.7;
  }
}

// ============================================
// Footer
// ============================================
.footer {
  background: $bg-oat;
  padding: 60px 0 30px;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 60px;
  margin-bottom: 50px;
}

.footer-brand {
  max-width: 300px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.footer-logo-icon {
  font-size: 28px;
}

.footer-logo-text {
  font-size: 20px;
  font-weight: 600;
  color: $brand-brown;
}

.footer-desc {
  font-size: 14px;
  color: $text-secondary;
  line-height: 1.8;
}

.footer-column {
  h4 {
    font-size: 14px;
    font-weight: 600;
    color: $text-primary;
    margin-bottom: 20px;
    letter-spacing: 1px;
  }

  ul {
    list-style: none;
  }

  li {
    margin-bottom: 12px;
  }

  a {
    color: $text-secondary;
    font-size: 14px;
    transition: color 0.3s ease;
    text-decoration: none;

    &:hover { color: $brand-brown; }
  }
}

.footer-bottom {
  border-top: 1px solid rgba(166, 139, 122, 0.2);
  padding-top: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;

  p {
    font-size: 13px;
    color: $text-secondary;
  }
}

.footer-social {
  display: flex;
  gap: 16px;

  span {
    width: 36px; height: 36px;
    background: $bg-white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    transition: all 0.3s ease;
    cursor: pointer;
    color: $brand-brown;

    &:hover {
      background: $brand-nude;
      color: white;
      transform: translateY(-3px);
    }
  }
}

// ============================================
// Responsive
// ============================================
@media (max-width: 1024px) {
  .destinations-grid { grid-template-columns: repeat(2, 1fr); }
  .rec-grid { grid-template-columns: repeat(2, 1fr); }
  .features-grid { grid-template-columns: repeat(2, 1fr); }
  .footer-content { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .hero { padding: 60px 0 80px; }
  .hero-title { font-size: 36px; }
  .destinations-grid { grid-template-columns: 1fr; }
  .rec-grid { grid-template-columns: 1fr; }
  .features-grid { grid-template-columns: 1fr; }
  .footer-content { grid-template-columns: 1fr; gap: 30px; }
}
</style>
