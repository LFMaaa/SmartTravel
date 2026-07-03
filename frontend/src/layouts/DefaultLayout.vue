<template>
  <div class="sidebar-layout">
    <!-- Left Sidebar Navigation -->
    <aside class="sidebar" :class="{ collapsed: isCollapsed }">
      <!-- Logo -->
      <div class="sidebar-brand" @click="$router.push('/')">
        <div class="brand-icon">🌿</div>
        <transition name="fade-text">
          <div v-show="!isCollapsed" class="brand-text">
            <span class="brand-name">旅游AI</span>
            <span class="brand-sub">SmartTravel</span>
          </div>
        </transition>
      </div>

      <!-- Navigation Links -->
      <nav class="sidebar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: isActive(item) }"
          :title="item.label"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <transition name="fade-text">
            <span v-show="!isCollapsed" class="nav-label">{{ item.label }}</span>
          </transition>
          <span v-if="item.badge && !isCollapsed" class="nav-badge">{{ item.badge }}</span>
        </router-link>
      </nav>

      <!-- AI Assistant Button -->
      <div class="sidebar-ai">
        <button class="ai-btn" @click="handleAIAssistant" :title="'AI助手'">
          <span class="ai-btn-icon">✨</span>
          <transition name="fade-text">
            <span v-show="!isCollapsed" class="ai-btn-text">AI 助手</span>
          </transition>
        </button>
      </div>

      <!-- User Section -->
      <div class="sidebar-user">
        <template v-if="userStore.isLoggedIn">
          <div class="user-info" @click="toggleUserMenu">
            <div class="user-avatar-sm">
              <span>{{ (userStore.user?.nickname || '用')[0] }}</span>
            </div>
            <transition name="fade-text">
              <div v-show="!isCollapsed" class="user-meta">
                <span class="user-name">{{ userStore.user?.nickname || '用户' }}</span>
                <span class="user-role">旅行者</span>
              </div>
            </transition>
          </div>
          <transition name="menu-slide">
            <div v-if="userMenuOpen && !isCollapsed" class="user-menu">
              <div class="menu-item" @click="navigateTo('/user')">
                <span>👤</span> 用户中心
              </div>
              <div class="menu-item" @click="navigateTo('/user/itineraries')">
                <span>📋</span> 我的行程
              </div>
              <div class="menu-item" @click="navigateTo('/user/orders')">
                <span>📦</span> 我的订单
              </div>
              <div class="menu-item" @click="navigateTo('/user/member')">
                <span>💎</span> 会员中心
              </div>
              <div class="menu-divider"></div>
              <div class="menu-item logout" @click="handleLogout">
                <span>🚪</span> 退出登录
              </div>
            </div>
          </transition>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-item" title="登录">
            <span class="nav-icon">🔑</span>
            <transition name="fade-text">
              <span v-show="!isCollapsed" class="nav-label">登录</span>
            </transition>
          </router-link>
        </template>
      </div>

      <!-- Collapse Toggle -->
      <button class="sidebar-toggle" @click="isCollapsed = !isCollapsed" :title="isCollapsed ? '展开' : '收起'">
        <span class="toggle-icon">{{ isCollapsed ? '▶' : '◀' }}</span>
      </button>
    </aside>

    <!-- Main Content Area -->
    <main class="main-area">
      <router-view v-slot="{ Component, route }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" :key="route.path" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapsed = ref(false)
const userMenuOpen = ref(false)

const navItems = [
  { path: '/', label: '首页', icon: '🏠' },
  { path: '/itinerary/generate', label: 'AI 规划', icon: '🤖', badge: 'AI' },
  { path: '/search', label: '探索', icon: '🔍' },
  { path: '/user/member', label: 'Pro 会员', icon: '💎' },
]

function isActive(item: typeof navItems[0]) {
  if (item.path === '/') return route.path === '/'
  return route.path.startsWith(item.path)
}

function handleAIAssistant() {
  router.push('/itinerary/generate')
}

function toggleUserMenu() {
  if (isCollapsed.value) {
    router.push('/user')
    return
  }
  userMenuOpen.value = !userMenuOpen.value
}

function navigateTo(path: string) {
  userMenuOpen.value = false
  router.push(path)
}

function handleLogout() {
  userMenuOpen.value = false
  userStore.logout()
  router.push('/')
}

function closeUserMenu(e: MouseEvent) {
  const target = e.target as HTMLElement
  if (!target.closest('.sidebar-user')) {
    userMenuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', closeUserMenu)
})

onUnmounted(() => {
  document.removeEventListener('click', closeUserMenu)
})
</script>

<style scoped lang="scss">
// ============================================
// Design Tokens — Earth & Elegance
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
$border-light: rgba(166, 139, 122, 0.12);

.sidebar-layout {
  display: flex;
  min-height: 100vh;
  background: $bg-warm;
}

// ============================================
// Sidebar
// ============================================
.sidebar {
  width: 240px;
  min-height: 100vh;
  background: $bg-oat;
  border-right: 1px solid $border;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  z-index: 50;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 1px 0 20px rgba(166, 139, 122, 0.08);
  overflow: hidden;

  &.collapsed {
    width: 72px;

    .sidebar-brand { padding: 24px 16px; justify-content: center; }
    .brand-icon { font-size: 26px; }
    .nav-item { justify-content: center; padding: 14px 12px; }
    .sidebar-ai { padding: 12px; }
    .ai-btn { justify-content: center; border-radius: 16px; width: 48px; height: 48px; padding: 0; }
    .sidebar-user { padding: 12px; }
    .user-info { justify-content: center; padding: 8px; }
    .user-meta { display: none; }
  }
}

// Brand
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 24px 20px 32px;
  cursor: pointer;
  user-select: none;
}

.brand-icon {
  font-size: 28px;
  line-height: 1;
  flex-shrink: 0;
}

.brand-text {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.brand-name {
  font-size: 20px;
  font-weight: 600;
  color: $brand-brown;
  letter-spacing: 1px;
  line-height: 1.2;
}

.brand-sub {
  font-size: 9px;
  color: $text-muted;
  letter-spacing: 2px;
  font-weight: 500;
}

// Navigation
.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 0 12px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 14px;
  text-decoration: none;
  color: $text-secondary;
  font-size: 15px;
  font-weight: 400;
  transition: all 0.25s ease;
  position: relative;
  white-space: nowrap;

  &:hover {
    background: rgba(166, 139, 122, 0.06);
    color: $brand-brown;
  }

  &.active {
    background: linear-gradient(135deg, rgba(232, 213, 208, 0.3) 0%, rgba(184, 196, 184, 0.25) 100%);
    color: $brand-brown;
    font-weight: 500;
    box-shadow: 0 4px 14px rgba(166, 139, 122, 0.08);

    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 50%;
      transform: translateY(-50%);
      width: 3px;
      height: 20px;
      background: linear-gradient(180deg, $brand-nude, $brand-sage);
      border-radius: 0 3px 3px 0;
    }
  }
}

.nav-icon {
  font-size: 20px;
  line-height: 1;
  flex-shrink: 0;
  width: 24px;
  text-align: center;
}

.nav-label {
  flex: 1;
}

.nav-badge {
  font-size: 10px;
  font-weight: 700;
  background: linear-gradient(135deg, $brand-nude 0%, $brand-sage 100%);
  color: white;
  padding: 2px 8px;
  border-radius: 10px;
  letter-spacing: 0.5px;
}

// AI Button
.sidebar-ai {
  padding: 16px 12px;
}

.ai-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  background: linear-gradient(135deg, $brand-nude 0%, $brand-sage 100%);
  border: none;
  border-radius: 16px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
  white-space: nowrap;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(184, 196, 184, 0.4);
  }

  &:active {
    transform: translateY(0);
  }
}

.ai-btn-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.ai-btn-text {
  letter-spacing: 0.5px;
}

// User Section
.sidebar-user {
  padding: 12px;
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 14px;
  cursor: pointer;
  transition: background 0.25s ease;

  &:hover {
    background: rgba(166, 139, 122, 0.06);
  }
}

.user-avatar-sm {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, $brand-nude 0%, $brand-sage 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
  border: 2px solid rgba(232, 213, 208, 0.5);
}

.user-meta {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: $text-primary;
  line-height: 1.3;
}

.user-role {
  font-size: 11px;
  color: $text-muted;
}

// User Dropdown Menu
.user-menu {
  position: absolute;
  bottom: 100%;
  left: 12px;
  right: 12px;
  margin-bottom: 4px;
  background: $bg-white;
  border-radius: 16px;
  padding: 8px;
  box-shadow: 0 8px 30px rgba(166, 139, 122, 0.12);
  border: 1px solid $border;
  z-index: 100;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 10px;
  cursor: pointer;
  color: $text-secondary;
  font-size: 14px;
  font-weight: 400;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(166, 139, 122, 0.06);
    color: $brand-brown;
  }

  &.logout:hover {
    background: rgba(212, 117, 107, 0.1);
    color: #D4756B;
  }

  span { font-size: 16px; }
}

.menu-divider {
  height: 1px;
  background: $border;
  margin: 4px 8px;
}

// Toggle Button
.sidebar-toggle {
  position: absolute;
  bottom: 20px;
  right: -12px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid $border;
  background: $bg-white;
  color: $text-muted;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  transition: all 0.25s ease;
  box-shadow: 0 2px 8px rgba(166, 139, 122, 0.08);
  z-index: 10;

  &:hover {
    color: $brand-brown;
    border-color: $brand-brown;
    box-shadow: 0 4px 12px rgba(166, 139, 122, 0.12);
  }
}

// ============================================
// Main Content Area
// ============================================
.main-area {
  flex: 1;
  min-width: 0;
  overflow-x: hidden;
}

// ============================================
// Transitions
// ============================================
.fade-text-enter-active,
.fade-text-leave-active {
  transition: opacity 0.2s ease;
}
.fade-text-enter-from,
.fade-text-leave-to {
  opacity: 0;
}

.menu-slide-enter-active {
  animation: menu-in 0.2s ease-out;
}
.menu-slide-leave-active {
  animation: menu-in 0.15s ease-in reverse;
}

@keyframes menu-in {
  from {
    opacity: 0;
    transform: translateY(8px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.page-fade-enter-from {
  opacity: 0;
  transform: translateX(8px);
}
.page-fade-leave-to {
  opacity: 0;
  transform: translateX(-8px);
}

// ============================================
// Responsive
// ============================================
@media (max-width: 768px) {
  .sidebar {
    width: 72px;
    &.collapsed { width: 0; padding: 0; border: none; overflow: hidden; }
  }
  .sidebar-toggle { display: none; }
}
</style>
