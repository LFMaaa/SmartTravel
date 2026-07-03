<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <router-link to="/" class="footer-logo">
          <div class="logo-mark">
            <svg viewBox="0 0 40 40" fill="none"><path d="M20 4C12.82 4 7 9.82 7 17c0 9.5 13 19 13 19s13-9.5 13-19c0-7.18-5.82-13-13-13zm0 17.5a4.5 4.5 0 110-9 4.5 4.5 0 010 9z" fill="currentColor"/></svg>
          </div>
          <div>
            <span class="footer-logo-text">智游</span>
            <span class="footer-logo-sub">SmartTravel</span>
          </div>
        </router-link>
        <p class="footer-desc">AI 驱动的智能旅行行程规划平台</p>
      </div>
      <div class="footer-links">
        <div class="link-group">
          <h4>功能</h4>
          <router-link to="/itinerary/generate">AI 行程规划</router-link>
          <router-link to="/search">探索目的地</router-link>
        </div>
        <div class="link-group">
          <h4>我的</h4>
          <router-link to="/user/itineraries">我的行程</router-link>
          <router-link to="/user/orders">我的订单</router-link>
          <router-link to="/user/settings">偏好设置</router-link>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 智游 SmartTravel. All rights reserved.</span>
    </div>
  </footer>
</template>

<style scoped lang="scss">
$bg-warm: #FAF8F3;
$bg-white: #FFFFFF;
$brand-brown: #A68B7A;
$brand-sage: #B8C4B8;
$text-primary: #3D3D3D;
$text-secondary: #6B6B6B;
$text-muted: #B8B0A8;
$border: #E8D5D0;

.app-footer {
  background: $bg-white;
  border-top: 1px solid $border;
  margin-top: auto;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-2xl) var(--space-lg);
  display: flex;
  justify-content: space-between;
  gap: var(--space-2xl);
}

.footer-brand {
  max-width: 300px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  margin-bottom: var(--space-md);

  .logo-mark {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #0f172a;
  }

  .footer-logo-text {
    display: block;
    font-size: 18px;
    font-weight: 800;
    color: $text-primary;
    line-height: 1.1;
  }

  .footer-logo-sub {
    font-size: 9px;
    color: $text-muted;
    letter-spacing: 2px;
  }
}

.footer-desc {
  font-size: 13px;
  color: $text-muted;
  line-height: 1.6;
}

.footer-links {
  display: flex;
  gap: var(--space-3xl);
}

.link-group {
  h4 {
    color: $text-primary;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: var(--space-md);
  }

  a {
    display: block;
    color: $text-muted;
    font-size: 13px;
    padding: 5px 0;
    transition: color 0.2s;
    text-decoration: none;

    &:hover { color: $brand-brown; }
  }
}

.footer-bottom {
  border-top: 1px solid $border;
  text-align: center;
  padding: var(--space-lg);
  font-size: var(--font-size-xs);
  color: $text-muted;
}

@media (max-width: 768px) {
  .footer-inner { flex-direction: column; gap: var(--space-xl); }
  .footer-links { gap: var(--space-xl); }
}
</style>
