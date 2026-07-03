<template>
  <div class="member-center">
    <!-- Hero -->
    <div class="member-hero">
      <div class="hero-bg">
        <div class="hero-orb orb-a"></div>
        <div class="hero-orb orb-b"></div>
      </div>
      <div class="hero-content">
        <div class="hero-icon">
          <svg viewBox="0 0 24 24" fill="currentColor" width="40" height="40"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
        </div>
        <h1>智游 Pro 会员</h1>
        <p>解锁全部智能旅行功能，让每一次旅程都完美</p>
        <button v-if="!userStore.user?.is_pro" class="hero-btn" :disabled="paying" @click="handlePayClick">
          <svg v-if="!paying" viewBox="0 0 20 20" fill="currentColor" width="18" height="18"><path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/></svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" class="spinning"><circle cx="12" cy="12" r="10" stroke-opacity="0.25"/><path d="M12 2a10 10 0 019.95 9" stroke-linecap="round"/></svg>
          {{ paying ? '处理中...' : '立即开通 ¥99/年' }}
        </button>
        <div v-else class="hero-badge-pro">
          <svg viewBox="0 0 20 20" fill="currentColor" width="20" height="20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
          您已是 Pro 会员
        </div>
      </div>
    </div>

    <!-- Benefits -->
    <div class="member-body container">
      <div class="section-header">
        <span class="section-overline">
          <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14" style="margin-right:6px"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
          会员权益
        </span>
        <h2 class="section-title">为什么选择 Pro？</h2>
        <div class="section-line"></div>
      </div>

      <div class="benefits-grid">
        <div v-for="b in benefits" :key="b.title" class="benefit-card">
          <div class="benefit-icon" :style="{ background: b.gradient }" v-html="b.icon"></div>
          <h3>{{ b.title }}</h3>
          <p>{{ b.desc }}</p>
        </div>
      </div>

      <!-- Comparison -->
      <div class="section-header compare-header-section" ref="plansRef">
        <span class="section-overline">
          <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14" style="margin-right:6px"><path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 6a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 6a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/></svg>
          对比
        </span>
        <h2 class="section-title">免费版 vs Pro</h2>
        <div class="section-line"></div>
      </div>

      <div class="compare-cards">
        <!-- Free -->
        <div class="compare-card free-card">
          <h3>
            <svg viewBox="0 0 20 20" fill="currentColor" width="20" height="20" style="vertical-align:-4px;margin-right:6px"><path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/></svg>
            免费版
          </h3>
          <div class="compare-price">¥0</div>
          <p class="compare-sub">适合偶尔出行的用户</p>
          <ul>
            <li v-for="f in freeFeatures" :key="f">
              <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
              {{ f }}
            </li>
          </ul>
        </div>

        <!-- Pro -->
        <div class="compare-card pro-card">
          <div class="pro-ribbon">推荐</div>
          <h3>
            <svg viewBox="0 0 20 20" fill="currentColor" width="20" height="20" style="vertical-align:-4px;margin-right:6px"><path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812z" clip-rule="evenodd"/></svg>
            Pro 版
          </h3>
          <div class="compare-price">¥99<span>/年</span></div>
          <p class="compare-sub">无限使用，解锁全部功能</p>
          <ul>
            <li v-for="f in proFeatures" :key="f">
              <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              {{ f }}
            </li>
          </ul>
          <button v-if="!userStore.user?.is_pro" class="pro-btn" :disabled="paying" @click="handlePayClick">
            {{ paying ? '处理中...' : '立即开通 Pro' }}
          </button>
          <div v-else class="pro-activated">
            <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
            已开通
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { paymentAPI } from '@/api/payment'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const plansRef = ref<HTMLElement | null>(null)
const paying = ref(false)

function scrollToPlans() { plansRef.value?.scrollIntoView({ behavior: 'smooth' }) }

async function handlePayClick() {
  if (paying.value) return
  if (!userStore.user?.id) {
    router.push('/login?redirect=/user/member')
    return
  }

  // 已是 Pro 会员
  if (userStore.user.is_pro) {
    return
  }

  paying.value = true
  // 保底定时器：1秒后强制复位，确保任何情况下按钮都不会一直转圈
  const guardTimer = setTimeout(() => { paying.value = false }, 1000)
  try {
    const { data } = await paymentAPI.createMemberOrder(userStore.user.id)
    const result = data.data

    if (result.alipay_url) {
      // 直接在当前页面跳转到支付宝沙箱（不开新标签页，避免拦截问题）
      window.location.href = result.alipay_url
      // 跳转后页面离开，保底定时器会在页面卸载时自动清理
      return
    } else {
      handleSandboxPay(result.order_id)
    }
  } catch (err: any) {
    console.error('支付下单失败:', err)
  } finally {
    clearTimeout(guardTimer)
    paying.value = false
  }
}

async function handleSandboxPay(orderId: string) {
  // 沙箱模拟支付：短暂延迟后确认支付成功
  await new Promise(resolve => setTimeout(resolve, 2000))

  try {
    await paymentAPI.sandboxPayMember(orderId)
    await userStore.fetchUser()
    paying.value = false
    alert('支付成功！您已升级为 Pro 会员，尽情享受全部智能旅行功能吧！')
    router.replace('/user/member')
  } catch (err: any) {
    paying.value = false
    alert(err?.response?.data?.detail || '支付确认失败，请查看订单状态')
  }
}

// 从支付宝返回时检查支付结果
onMounted(async () => {
  const paid = route.query.paid
  const orderId = route.query.order_id as string

  if (paid === '1' && orderId && userStore.user) {
    // 从支付宝返回，刷新用户信息获取最新会员状态
    await userStore.fetchUser()
    if (userStore.user.is_pro) {
      alert('支付成功！您已升级为 Pro 会员，尽情享受全部智能旅行功能吧！')
    }
    // 清除 URL 参数
    router.replace('/user/member')
  }
})

const benefits = [
  { icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:26px;height:26px"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>`, gradient: 'linear-gradient(135deg, #f59e0b, #d97706)', title: '无限行程生成', desc: '不限次数使用 AI 智能规划行程，想规划多少次都可以' },
  { icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:26px;height:26px"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>`, gradient: 'linear-gradient(135deg, #3b82f6, #2563eb)', title: '动态实时重规划', desc: '遇到航班延误、天气变化，AI 自动生成备选方案' },
  { icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:26px;height:26px"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>`, gradient: 'linear-gradient(135deg, #10b981, #059669)', title: '深度定制', desc: '更精准的偏好匹配，个性化推荐专属行程' },
  { icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:26px;height:26px"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`, gradient: 'linear-gradient(135deg, #8b5cf6, #7c3aed)', title: '优先预订', desc: '热门酒店、门票优先占位，无需排队等待' },
  { icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:26px;height:26px"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M9 4v16"/><path d="M2 8h4"/><path d="M18 8h4"/><path d="M2 12h20"/><path d="M12 4v16"/></svg>`, gradient: 'linear-gradient(135deg, #ef4444, #dc2626)', title: '会员折扣', desc: '预订酒店、门票享专属会员折扣价' },
  { icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:26px;height:26px"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/><circle cx="9" cy="10" r="1"/><circle cx="15" cy="10" r="1"/></svg>`, gradient: 'linear-gradient(135deg, #06b6d4, #0891b2)', title: '7×24 专属客服', desc: '旅行中遇到任何问题，随时获得人工帮助' },
]

const freeFeatures = ['3个行程额度', '基础 AI 生成', '标准搜索', '基础偏好设置']
const proFeatures = ['无限行程生成', '动态实时重规划', '深度定制推荐', '优先预订占位', '会员专属折扣', '7×24 专属客服']
</script>

<style scoped lang="scss">
$bg-warm: #FAF8F3;
$bg-white: #FFFFFF;
$bg-oat: #F5F0E8;
$brand-brown: #A68B7A;
$brand-brown-light: #C4A89A;
$brand-sage: #B8C4B8;
$text-primary: #3D3D3D;
$text-secondary: #6B6B6B;
$text-muted: #B8B0A8;
$border: #E8D5D0;

.member-center {
  background: $bg-warm;
  min-height: 100vh;
}

// ============================================
// Hero — same pattern as SearchView
// ============================================
.member-hero {
  position: relative; overflow: hidden;
  padding: 64px 24px 56px;
  text-align: center;
  background: $bg-white;
  border-bottom: 1px solid $border;
}

.hero-bg { position: absolute; inset: 0; }
.hero-orb {
  position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.07;
  &.orb-a { width: 350px; height: 350px; background: #f59e0b; top: -120px; right: -80px; }
  &.orb-b { width: 300px; height: 300px; background: #3b82f6; bottom: -100px; left: -80px; }
}

.hero-content { position: relative; z-index: 1; }

.hero-icon {
  width: 72px; height: 72px; margin: 0 auto 20px;
  background: linear-gradient(135deg, rgba(245,158,11,0.15), rgba(245,158,11,0.05));
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: 20px;
  display: flex; align-items: center; justify-content: center;
  color: $brand-brown;
}

.hero-content h1 {
  font-size: 34px; font-weight: 800; color: $text-primary; margin-bottom: 10px;
}

.hero-content > p {
  font-size: 16px; color: $text-muted; margin-bottom: 28px;
}

.hero-btn {
  padding: 14px 36px; border: none; border-radius: 14px;
  font-size: 16px; font-weight: 700; font-family: inherit;
  cursor: pointer; color: #0f172a;
  background: linear-gradient(135deg, $brand-brown-light, $brand-brown);
  box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
  display: inline-flex; align-items: center; gap: 8px;
  transition: all 0.3s ease;
  &:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(245, 158, 11, 0.45); }
  &:disabled { opacity: 0.65; cursor: not-allowed; transform: none; }
}

.spinning { animation: spin 0.8s linear infinite; }
@keyframes spin { 100% { transform: rotate(360deg); } }

.hero-badge-pro {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 14px 36px; border-radius: 14px;
  font-size: 16px; font-weight: 700;
  color: #10b981;
  background: rgba(16, 185, 129, 0.08);
  border: 1.5px solid rgba(16, 185, 129, 0.2);
}

// ============================================
// Body
// ============================================
.member-body { padding-bottom: 80px; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 24px; }

.section-header { text-align: center; margin-top: 56px; margin-bottom: 36px; }
.section-overline {
  display: inline-block; font-size: 12px; font-weight: 700;
  letter-spacing: 3px; text-transform: uppercase;
  color: $brand-brown; margin-bottom: 10px;
  background: rgba(245,158,11,0.08); padding: 4px 14px;
  border-radius: 20px; border: 1px solid rgba(245,158,11,0.15);
}
.section-title { font-size: 28px; font-weight: 700; color: $text-primary; }
.section-line {
  width: 48px; height: 3px;
  background: linear-gradient(90deg, $brand-brown, transparent);
  border-radius: 2px; margin: 14px auto 0;
}

// ============================================
// Benefits Grid
// ============================================
.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 18px;
}

.benefit-card {
  padding: 28px 22px;
  background: $bg-oat;
  border-radius: 16px;
  border: 1px solid $border;
  text-align: center;
  transition: all 0.3s ease;

  &:hover {
    border-color: rgba(245,158,11,0.25);
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.35);
  }

  .benefit-icon {
    width: 52px; height: 52px; border-radius: 14px;
    display: inline-flex; align-items: center; justify-content: center;
    color: #fff; margin-bottom: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  }

  h3 { font-size: 16px; font-weight: 600; color: $text-primary; margin-bottom: 6px; }
  p { font-size: 13px; color: $text-muted; line-height: 1.6; }
}

// ============================================
// Compare Cards
// ============================================
.compare-header-section { margin-top: 64px; }

.compare-cards {
  display: flex; gap: 22px;
  max-width: 700px; margin: 0 auto;
}

.compare-card {
  flex: 1; padding: 36px 26px 28px;
  border-radius: 18px; text-align: center;
  position: relative; overflow: hidden;
  transition: all 0.3s ease;

  h3 { font-size: 20px; font-weight: 700; margin-bottom: 12px; }

  .compare-price {
    font-size: 44px; font-weight: 800; margin-bottom: 6px; line-height: 1;
    span { font-size: 14px; font-weight: 400; opacity: 0.6; }
  }

  .compare-sub {
    font-size: 13px; margin-bottom: 22px;
  }

  ul {
    list-style: none; text-align: left;
    li {
      display: flex; align-items: center; gap: 10px;
      padding: 7px 0; font-size: 14px;
      svg { flex-shrink: 0; }
    }
  }
}

// Free card
.free-card {
  background: $bg-white;
  border: 1px solid $border;
  h3 { color: $text-muted; }
  .compare-price { color: $text-muted; }
  .compare-sub { color: $text-muted; }
  ul li { color: $text-muted; svg { color: $text-muted; } }
}

// Pro card
.pro-card {
  background: linear-gradient(160deg, #1a2744, #142038);
  border: 1.5px solid rgba(245, 158, 11, 0.4);
  box-shadow: 0 0 50px rgba(245, 158, 11, 0.06), 0 8px 32px rgba(0,0,0,0.4);

  h3 { color: $brand-brown; }
  .compare-price { color: $brand-brown; }
  .compare-sub { color: $text-secondary; }
  ul li { color: $text-secondary; svg { color: #10b981; } }

  &:hover {
    border-color: rgba(245, 158, 11, 0.55);
    box-shadow: 0 0 60px rgba(245, 158, 11, 0.1), 0 12px 40px rgba(0,0,0,0.5);
    transform: translateY(-2px);
  }
}

.pro-ribbon {
  position: absolute; top: 14px; right: -30px;
  padding: 4px 36px;
  background: $brand-brown;
  color: #0f172a;
  font-size: 11px; font-weight: 700;
  transform: rotate(45deg);
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.pro-btn {
  width: 100%; margin-top: 24px;
  padding: 14px 0; border: none; border-radius: 12px;
  font-size: 16px; font-weight: 700; font-family: inherit;
  cursor: pointer; color: #0f172a;
  background: linear-gradient(135deg, $brand-brown-light, $brand-brown);
  box-shadow: 0 4px 16px rgba(245,158,11,0.25);
  transition: all 0.3s ease;
  &:hover { transform: translateY(-1px); box-shadow: 0 6px 24px rgba(245,158,11,0.4); }
  &:disabled { opacity: 0.65; cursor: not-allowed; transform: none; }
}

.pro-activated {
  width: 100%; margin-top: 24px; padding: 14px 0;
  border-radius: 12px; text-align: center;
  font-size: 16px; font-weight: 700;
  color: #10b981;
  background: rgba(16, 185, 129, 0.08);
  border: 1.5px solid rgba(16, 185, 129, 0.2);
  display: flex; align-items: center; justify-content: center; gap: 6px;
}

@media (max-width: 768px) {
  .compare-cards { flex-direction: column; }
  .member-hero { padding: 48px 20px; }
  .hero-content h1 { font-size: 26px; }
}
</style>
