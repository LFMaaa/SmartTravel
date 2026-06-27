<template>
  <header class="app-header">
    <div class="header-inner">
      <router-link to="/" class="header-logo">
        <div class="logo-mark">
          <svg viewBox="0 0 40 40" fill="none">
            <path d="M20 4C12.82 4 7 9.82 7 17c0 9.5 13 19 13 19s13-9.5 13-19c0-7.18-5.82-13-13-13zm0 17.5a4.5 4.5 0 110-9 4.5 4.5 0 010 9z" fill="currentColor"/>
          </svg>
        </div>
        <span class="logo-text">智游</span>
        <span class="logo-sub">SmartTravel</span>
      </router-link>

      <nav class="header-nav">
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">首页</router-link>
        <router-link to="/itinerary/generate" class="nav-link" active-class="active">AI 规划</router-link>
        <router-link to="/search" class="nav-link" active-class="active">探索</router-link>
        <router-link to="/user/member" class="nav-link" :class="{ active: $route.path === '/user/member' }">Pro 会员</router-link>
        <router-link to="/user" class="nav-link" :class="{ active: $route.path === '/user' || ($route.path.startsWith('/user/') && $route.path !== '/user/member') }">我的</router-link>
      </nav>

      <div class="header-actions">
        <el-badge :value="notificationStore.unreadCount" :hidden="notificationStore.unreadCount === 0">
          <button class="icon-btn" @click="$router.push('/user')">
            <svg viewBox="0 0 20 20" fill="currentColor"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/></svg>
          </button>
        </el-badge>

        <template v-if="userStore.isLoggedIn">
          <div class="user-dropdown" :class="{ open: dropdownOpen }">
            <div class="user-trigger" @click="toggleDropdown">
              <div class="user-avatar">
                <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/></svg>
              </div>
              <span class="user-name">{{ userStore.user?.nickname || '用户' }}</span>
              <svg viewBox="0 0 20 20" fill="currentColor" class="dropdown-arrow" :class="{ rotated: dropdownOpen }"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
            </div>
            <transition name="dropdown-fade">
              <div v-if="dropdownOpen" class="dropdown-panel" @click.stop>
                <div class="dropdown-item" @click="navigateTo('/user')">
                  <div class="dropdown-icon user-center-icon">
                    <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/></svg>
                  </div>
                  <span>用户中心</span>
                </div>
                <div class="dropdown-item" @click="navigateTo('/user/itineraries')">
                  <div class="dropdown-icon itinerary-icon">
                    <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd"/></svg>
                  </div>
                  <span>我的行程</span>
                </div>
                <div class="dropdown-item" @click="navigateTo('/user/orders')">
                  <div class="dropdown-icon orders-icon">
                    <svg viewBox="0 0 20 20" fill="currentColor"><path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z"/><path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd"/></svg>
                  </div>
                  <span>我的订单</span>
                </div>
                <div class="dropdown-divider"></div>
                <div class="dropdown-item logout-item" @click="handleLogout">
                  <div class="dropdown-icon logout-icon">
                    <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd"/></svg>
                  </div>
                  <span>退出登录</span>
                </div>
              </div>
            </transition>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="btn-login">登录</router-link>
          <router-link to="/register" class="btn-register">免费注册</router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useNotificationStore } from '@/stores/notification'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const notificationStore = useNotificationStore()
const router = useRouter()

const dropdownOpen = ref(false)

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value
}

function navigateTo(path: string) {
  dropdownOpen.value = false
  router.push(path)
}

function handleLogout() {
  dropdownOpen.value = false
  userStore.logout()
  router.push('/')
}

function closeDropdown(e: MouseEvent) {
  const target = e.target as HTMLElement
  if (!target.closest('.user-dropdown')) {
    dropdownOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', closeDropdown)
})

onUnmounted(() => {
  document.removeEventListener('click', closeDropdown)
})
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

.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(10, 14, 26, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  height: 64px;
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
  height: 100%;
  display: flex;
  align-items: center;
  gap: var(--space-xl);
}

.header-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  flex-shrink: 0;

  .logo-mark {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #0f172a;
  }

  .logo-text {
    font-size: 20px;
    font-weight: 800;
    color: $text-primary;
    letter-spacing: 1px;
  }

  .logo-sub {
    font-size: 9px;
    color: $text-muted;
    font-weight: 600;
    letter-spacing: 2px;
    margin-top: 2px;
  }
}

.header-nav {
  display: flex;
  gap: 2px;
  flex: 1;

  .nav-link {
    padding: 8px 18px;
    font-size: 14px;
    font-weight: 500;
    color: $text-secondary;
    text-decoration: none;
    border-radius: 10px;
    transition: all 0.25s ease;

    &:hover {
      color: $text-primary;
      background: rgba(255, 255, 255, 0.04);
    }

    &.active {
      color: $brand-amber;
      background: rgba(245, 158, 11, 0.08);
    }
  }

}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.icon-btn {
  width: 36px; height: 36px;
  border-radius: 10px;
  border: none;
  background: rgba(255, 255, 255, 0.04);
  color: $text-secondary;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;

  svg { width: 18px; height: 18px; }

  &:hover {
    background: rgba(245, 158, 11, 0.08);
    color: $brand-amber;
  }
}

.user-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 14px 4px 4px;
  border-radius: 12px;
  transition: background 0.25s ease;

  &:hover { background: rgba(255, 255, 255, 0.04); }
}

.user-dropdown {
  position: relative;
}

.dropdown-panel {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  min-width: 210px;
  background: $bg-card;
  border: 1px solid $border;
  border-radius: 16px;
  padding: 8px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.04) inset;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  z-index: 200;
  overflow: hidden;
  transform-origin: top right;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 10px;
  cursor: pointer;
  color: $text-secondary;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.05);
    color: $text-primary;
  }

  span { line-height: 1; }
}

.logout-item {
  &:hover {
    color: #f87171;
    background: rgba(239, 68, 68, 0.08);
  }
}

.dropdown-divider {
  height: 1px;
  background: $border;
  margin: 4px 8px;
}

.dropdown-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  svg { width: 16px; height: 16px; }
}

.user-center-icon {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.15));
  color: #8b9cf6;
}

.itinerary-icon {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(251, 191, 36, 0.15));
  color: $brand-amber;
}

.orders-icon {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(16, 185, 129, 0.15));
  color: #4ade80;
}

.logout-icon {
  background: rgba(239, 68, 68, 0.08);
  color: #f87171;
}

.user-avatar {
  width: 34px; height: 34px;
  border-radius: 10px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;

  svg { width: 18px; height: 18px; }
}

.user-name {
  font-size: 13px;
  font-weight: 500;
  color: $text-primary;
}

.dropdown-arrow {
  width: 14px; height: 14px;
  color: $text-muted;
  transition: transform 0.25s ease;

  &.rotated { transform: rotate(180deg); }
}

.btn-login {
  padding: 8px 20px;
  border-radius: 10px;
  border: 1.5px solid $border;
  color: $text-primary;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.25s ease;
  background: transparent;

  &:hover { border-color: $text-muted; }
}

.btn-register {
  padding: 8px 20px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: #0f172a;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.25s ease;
  box-shadow: 0 2px 10px rgba(245, 158, 11, 0.2);

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3);
  }
}

// Dropdown transition
.dropdown-fade-enter-active {
  animation: dropdown-in 0.2s ease-out;
}
.dropdown-fade-leave-active {
  animation: dropdown-in 0.15s ease-in reverse;
}

@keyframes dropdown-in {
  from {
    opacity: 0;
    transform: scale(0.92) translateY(-8px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@media (max-width: 768px) {
  .header-nav { display: none; }
  .btn-login, .btn-register { font-size: 13px; padding: 6px 14px; }
}
</style>
