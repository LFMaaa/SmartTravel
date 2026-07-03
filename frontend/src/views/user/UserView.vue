<template>
  <div class="user-container">
    <!-- Sidebar -->
    <aside class="user-sidebar">
      <div class="sidebar-header">
        <div class="logo-wrapper">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
          </div>
          <span class="logo-text">智游</span>
        </div>
      </div>

      <div class="sidebar-user">
        <div class="user-avatar">
          <div class="avatar-circle">
            <svg viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path fill-rule="evenodd" d="M18.685 19.097A9.723 9.723 0 0021.75 12c0-5.385-4.365-9.75-9.75-9.75S2.25 6.615 2.25 12a9.723 9.723 0 003.065 7.097A9.716 9.716 0 0012 21.75a9.716 9.716 0 006.685-2.653zm-12.54-1.285A7.486 7.486 0 0112 15a7.486 7.486 0 015.855 2.812A8.224 8.224 0 0112 20.25a8.224 8.224 0 01-5.855-2.438zM15.75 9a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" clip-rule="evenodd"/></svg>
          </div>
          <div class="avatar-badge"></div>
        </div>
        <div class="sidebar-user-info">
          <span class="sidebar-name">{{ userStore.user?.nickname || '旅行者' }}</span>
          <span class="sidebar-phone">
            <svg viewBox="0 0 16 16" fill="currentColor" width="12" height="12" style="vertical-align:-1px"><path fill-rule="evenodd" d="M1.885.511a1.745 1.745 0 012.61.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.678.678 0 00.178.643l2.457 2.457a.678.678 0 00.644.178l2.189-.547a1.745 1.745 0 011.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.634 18.634 0 01-7.01-4.42 18.634 18.634 0 01-4.42-7.009c-.362-1.03-.037-2.137.703-2.877L1.885.511z" clip-rule="evenodd"/></svg>
            {{ userStore.user?.phone || '' }}
          </span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/user" exact-active-class="active" end class="nav-item">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18">
              <rect x="3" y="3" width="7" height="7" rx="1"/>
              <rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/>
              <rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
          </div>
          <span>概览</span>
        </router-link>
        <router-link to="/user/itineraries" active-class="active" class="nav-item">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
              <circle cx="12" cy="10" r="3"/>
            </svg>
          </div>
          <span>我的行程</span>
        </router-link>
        <router-link to="/user/orders" active-class="active" class="nav-item">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18">
              <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
              <polyline points="10 9 9 9 8 9"/>
            </svg>
          </div>
          <span>我的订单</span>
        </router-link>
        <router-link to="/user/favorites" active-class="active" class="nav-item">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18">
              <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
            </svg>
          </div>
          <span>收藏</span>
        </router-link>
        <router-link to="/user/settings" active-class="active" class="nav-item">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/>
            </svg>
          </div>
          <span>偏好设置</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button class="logout-btn" @click="handleLogout">
          <svg viewBox="0 0 20 20" fill="currentColor" style="width: 18px; height: 18px;">
            <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd"/>
          </svg>
          <span>退出登录</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="user-main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

function handleLogout() {
  userStore.logout()
  router.push('/')
}
</script>

<style scoped lang="scss">
// 大地素雅风变量
$bg-warm: #FAF8F3;
$bg-white: #FFFFFF;
$bg-oat: #F5F0E8;
$brand-brown: #A68B7A;
$brand-sage: #B8C4B8;
$text-primary: #3D3D3D;
$text-secondary: #6B6B6B;
$text-muted: #B8B0A8;
$border: #E8D5D0;
$border-light: rgba(166, 139, 122, 0.08);

.user-container {
  min-height: calc(100vh - 64px);
  background: $bg-warm;
  display: flex;
  gap: 24px;
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

// Sidebar
.user-sidebar {
  width: 280px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: $bg-white;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
  padding: 32px 24px;
}

.sidebar-header {
  margin-bottom: 32px;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;

  .logo-icon {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
  }

  .logo-text {
    font-size: 22px;
    font-weight: 800;
    color: $text-primary;
  }
}

// User info
.sidebar-user {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-bottom: 24px;
  margin-bottom: 24px;
  border-bottom: 1px solid $border;
}

.user-avatar {
  position: relative;

  .avatar-circle {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
  }

  .avatar-badge {
    position: absolute;
    bottom: 2px;
    right: 2px;
    width: 14px;
    height: 14px;
    background: #48bb78;
    border-radius: 50%;
    border: 2px solid $bg-white;
  }
}

.sidebar-user-info {
  display: flex;
  flex-direction: column;
}

.sidebar-name {
  font-size: 16px;
  font-weight: 700;
  color: $text-primary;
  margin-bottom: 4px;
}

.sidebar-phone {
  font-size: 13px;
  color: $text-muted;
}

// Navigation
.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border-radius: 16px;
  font-size: 15px;
  font-weight: 500;
  color: $text-secondary;
  text-decoration: none;
  transition: all 0.3s ease;

  .nav-icon {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.05);
    color: $text-secondary;
    transition: all 0.3s ease;
  }

  &:hover {
    background: rgba(255, 255, 255, 0.06);
    color: $text-primary;

    .nav-icon {
      background: rgba(102, 126, 234, 0.15);
      color: #667eea;
    }
  }

  &.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-weight: 600;
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);

    .nav-icon {
      background: rgba(255, 255, 255, 0.2);
      color: white;
    }
  }
}

// Footer
.sidebar-footer {
  padding-top: 16px;
  border-top: 1px solid $border;
  margin-top: 16px;
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: flex-start;
  color: $text-muted;
  font-size: 14px;
  padding: 12px 16px;
  border-radius: 16px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
  }
}

// Main content
.user-main {
  flex: 1;
  min-width: 0;
  background: $bg-oat;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
  padding: 32px;
  overflow: auto;
}

// 响应式
@media (max-width: 768px) {
  .user-container {
    flex-direction: column;
    padding: 16px;
    gap: 16px;
  }

  .user-sidebar {
    width: 100%;
    padding: 20px;
  }

  .sidebar-user {
    display: none;
  }

  .sidebar-footer {
    display: none;
  }

  .sidebar-nav {
    flex-direction: row;
    gap: 8px;
    overflow-x: auto;
  }

  .nav-item {
    padding: 10px 14px;
    font-size: 13px;
    white-space: nowrap;
  }

  .user-main {
    padding: 20px;
  }
}
</style>

