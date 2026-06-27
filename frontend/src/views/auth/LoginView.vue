<template>
  <div class="auth-page">
    <!-- Decorative background elements -->
    <div class="bg-layer">
      <div class="bg-orb orb-1"></div>
      <div class="bg-orb orb-2"></div>
      <div class="bg-orb orb-3"></div>
      <div class="bg-grid"></div>
    </div>

    <div class="auth-card">
      <!-- Left: Brand Panel -->
      <div class="brand-panel">
        <div class="brand-glow"></div>
        <div class="brand-content">
          <!-- Logo -->
          <div class="brand-logo" @click="$router.push('/')">
            <div class="logo-mark">
              <svg viewBox="0 0 40 40" fill="none">
                <path d="M20 4C12.82 4 7 9.82 7 17c0 9.5 13 19 13 19s13-9.5 13-19c0-7.18-5.82-13-13-13zm0 17.5a4.5 4.5 0 110-9 4.5 4.5 0 010 9z" fill="currentColor"/>
              </svg>
            </div>
            <div class="logo-text">
              <span class="logo-cn">智游</span>
              <span class="logo-en">SMART TRAVEL</span>
            </div>
          </div>

          <!-- Hero text -->
          <div class="brand-hero">
            <h2 class="hero-title">
              <span class="hero-line">探索世界，</span>
              <span class="hero-line hero-accent">随心而行</span>
            </h2>
            <p class="hero-desc">AI 驱动的智能行程规划，让每一次出发都成为难忘的旅程</p>
          </div>

          <!-- Travel stats -->
          <div class="brand-stats">
            <div class="stat-item">
              <span class="stat-num">50+</span>
              <span class="stat-label">目的地覆盖</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-num">10万+</span>
              <span class="stat-label">智能行程已生成</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-num">98%</span>
              <span class="stat-label">用户好评率</span>
            </div>
          </div>

          <!-- Testimonial -->
          <div class="brand-quote">
            <svg class="quote-mark" viewBox="0 0 24 24" fill="currentColor" opacity="0.3">
              <path d="M6 17h3l2-4V7H5v6h3zm8 0h3l2-4V7h-6v6h3z"/>
            </svg>
            <p>"这是我用过最智能的旅行规划工具，AI 生成的行程完全超出了我的预期。"</p>
            <div class="quote-author">
              <div class="author-avatar">L</div>
              <div>
                <span class="author-name">旅行者小李</span>
                <span class="author-role">资深自由行爱好者</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Form Panel -->
      <div class="form-panel">
        <div class="form-container">
          <!-- Header -->
          <div class="form-header">
            <h3 class="form-title">欢迎回来</h3>
            <p class="form-subtitle">选择你喜欢的方式登录</p>
          </div>

          <!-- Tab Switcher -->
          <div class="auth-tabs">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              :class="['tab-item', { active: activeTab === tab.key }]"
              @click="switchTab(tab.key)"
            >
              <span class="tab-icon">
                <el-icon :size="18"><component :is="tab.icon" /></el-icon>
              </span>
              <span class="tab-label">{{ tab.label }}</span>
            </button>
            <div
              class="tab-indicator"
              :style="{ transform: `translateX(${tabs.findIndex(t => t.key === activeTab) * 100}%)` }"
            ></div>
          </div>

          <!-- Error Alert -->
          <transition name="alert">
            <div v-if="errorMsg" class="alert alert-error">
              <svg class="alert-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
              </svg>
              <span>{{ errorMsg }}</span>
              <button class="alert-close" @click="errorMsg = ''">
                <svg viewBox="0 0 16 16" fill="currentColor"><path d="M4.293 4.293a1 1 0 011.414 0L8 6.586l2.293-2.293a1 1 0 011.414 1.414L9.414 8l2.293 2.293a1 1 0 01-1.414 1.414L8 9.414l-2.293 2.293a1 1 0 01-1.414-1.414L6.586 8 4.293 5.707a1 1 0 010-1.414z"/></svg>
              </button>
            </div>
          </transition>

          <!-- SMS sent success -->
          <transition name="alert">
            <div v-if="smsSent" class="alert alert-success">
              <svg class="alert-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              <div>
                <p class="alert-title">验证码已发送</p>
                <p class="alert-desc">已发送至 {{ form.phone }}，有效期5分钟<span v-if="smsDevCode">（开发：{{ smsDevCode }}）</span></p>
              </div>
              <button class="alert-close" @click="smsSent = false">
                <svg viewBox="0 0 16 16" fill="currentColor"><path d="M4.293 4.293a1 1 0 011.414 0L8 6.586l2.293-2.293a1 1 0 011.414 1.414L9.414 8l2.293 2.293a1 1 0 01-1.414 1.414L8 9.414l-2.293 2.293a1 1 0 01-1.414-1.414L6.586 8 4.293 5.707a1 1 0 010-1.414z"/></svg>
              </button>
            </div>
          </transition>

          <!-- Registration success alert -->
          <transition name="alert">
            <div v-if="registerSuccess" class="alert alert-success">
              <svg class="alert-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              <div>
                <p class="alert-title">注册成功</p>
                <p class="alert-desc">账号 {{ registerPhone }} 已创建，请登录</p>
              </div>
              <button class="alert-close" @click="registerSuccess = false">
                <svg viewBox="0 0 16 16" fill="currentColor"><path d="M4.293 4.293a1 1 0 011.414 0L8 6.586l2.293-2.293a1 1 0 011.414 1.414L9.414 8l2.293 2.293a1 1 0 01-1.414 1.414L8 9.414l-2.293 2.293a1 1 0 01-1.414-1.414L6.586 8 4.293 5.707a1 1 0 010-1.414z"/></svg>
              </button>
            </div>
          </transition>

          <!-- ========== Password Login ========== -->
          <form v-if="activeTab === 'password'" class="auth-form" @submit.prevent="handlePasswordSubmit">
            <div class="input-group">
              <label class="input-label">手机号</label>
              <div class="input-wrapper">
                <span class="input-prefix">
                  <svg viewBox="0 0 20 20" fill="currentColor"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/></svg>
                </span>
                <input
                  v-model="form.phone"
                  type="tel"
                  class="input-field"
                  placeholder="请输入手机号"
                  maxlength="11"
                />
              </div>
            </div>

            <div class="input-group">
              <label class="input-label">密码</label>
              <div class="input-wrapper">
                <span class="input-prefix">
                  <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"/></svg>
                </span>
                <input
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="input-field"
                  placeholder="请输入密码"
                />
                <button type="button" class="input-suffix" @click="showPassword = !showPassword">
                  <svg v-if="!showPassword" viewBox="0 0 20 20" fill="currentColor"><path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/><path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/></svg>
                  <svg v-else viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd"/><path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z"/></svg>
                </button>
              </div>
            </div>

            <div class="form-extra">
              <label class="remember-me">
                <input type="checkbox" v-model="rememberMe" />
                <span class="checkmark"></span>
                <span>记住我</span>
              </label>
              <a class="forgot-link" @click.prevent="handleForgotPassword">忘记密码？</a>
            </div>

            <button type="submit" class="submit-btn" :disabled="loading">
              <span v-if="!loading">登 录</span>
              <span v-else class="btn-loading">
                <svg class="spinner" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="31.4 31.4" stroke-linecap="round"/></svg>
                登录中...
              </span>
            </button>
          </form>

          <!-- ========== SMS Login ========== -->
          <form v-if="activeTab === 'sms'" class="auth-form" @submit.prevent="handleSmsSubmit">
            <div class="input-group">
              <label class="input-label">手机号</label>
              <div class="input-wrapper">
                <span class="input-prefix">
                  <svg viewBox="0 0 20 20" fill="currentColor"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/></svg>
                </span>
                <input
                  v-model="form.phone"
                  type="tel"
                  class="input-field"
                  placeholder="请输入手机号"
                  maxlength="11"
                />
              </div>
            </div>

            <div class="input-group">
              <label class="input-label">验证码</label>
              <div class="sms-row">
                <div class="input-wrapper sms-input-wrap">
                  <span class="input-prefix">
                    <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"/></svg>
                  </span>
                  <input
                    v-model="form.smsCode"
                    type="text"
                    class="input-field"
                    placeholder="输入6位验证码"
                    maxlength="6"
                  />
                </div>
                <button
                  type="button"
                  class="sms-btn"
                  :disabled="smsCountdown > 0 || sendingSms"
                  @click="handleSendSms"
                >
                  <span v-if="sendingSms">
                    <svg class="spinner sm" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="31.4 31.4" stroke-linecap="round"/></svg>
                  </span>
                  <span v-else-if="smsCountdown > 0">{{ smsCountdown }}s 后重试</span>
                  <span v-else>获取验证码</span>
                </button>
              </div>
            </div>

            <button type="submit" class="submit-btn" :disabled="loading">
              <span v-if="!loading">登录 / 注册</span>
              <span v-else class="btn-loading">
                <svg class="spinner" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="31.4 31.4" stroke-linecap="round"/></svg>
                验证中...
              </span>
            </button>

            <p class="sms-hint">未注册手机号将自动创建账号</p>
          </form>

          <!-- ========== WeChat Login ========== -->
          <div v-if="activeTab === 'wechat'" class="auth-form">
            <div class="wechat-qr">
              <div class="qr-wrapper">
                <div class="qr-placeholder">
                  <svg viewBox="0 0 48 48" fill="none" class="qr-icon">
                    <rect x="4" y="4" width="16" height="16" rx="3" stroke="currentColor" stroke-width="2"/>
                    <rect x="28" y="4" width="16" height="16" rx="3" stroke="currentColor" stroke-width="2"/>
                    <rect x="4" y="28" width="16" height="16" rx="3" stroke="currentColor" stroke-width="2"/>
                    <rect x="9" y="9" width="6" height="6" fill="currentColor"/>
                    <rect x="33" y="9" width="6" height="6" fill="currentColor"/>
                    <rect x="9" y="33" width="6" height="6" fill="currentColor"/>
                    <circle cx="36" cy="36" r="4" stroke="currentColor" stroke-width="2"/>
                  </svg>
                  <p>请使用微信扫一扫</p>
                </div>
              </div>
            </div>

            <div class="divider">
              <span class="divider-line"></span>
              <span class="divider-text">或使用授权码登录</span>
              <span class="divider-line"></span>
            </div>

            <div class="input-group">
              <label class="input-label">微信授权码</label>
              <div class="input-wrapper">
                <span class="input-prefix">
                  <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11H9V9.83a3.001 3.001 0 01-2-2.83 3 3 0 012.824-2.995L10 4h.01a.999.999 0 01.99 1.007A1 1 0 0110 5a1 1 0 00-1 1 .993.993 0 001 1 .997.997 0 001-1 1 1 0 00-1-1zM9 13h2v2H9v-2z" clip-rule="evenodd"/></svg>
                </span>
                <input
                  v-model="form.wechatCode"
                  type="text"
                  class="input-field"
                  placeholder="输入授权码（开发环境任意字符）"
                />
              </div>
            </div>

            <button type="button" class="submit-btn wechat-btn" :disabled="loading" @click="handleWechatSubmit">
              <span v-if="!loading">
                <svg viewBox="0 0 20 20" fill="currentColor" class="wechat-logo"><path d="M6.5 7a1 1 0 100-2 1 1 0 000 2zm4 0a1 1 0 100-2 1 1 0 000 2zM2.4 2.9c3.2-2.6 8.1-2.1 10.7 1.2.2.3.1.7-.3.8-.4.1-.8-.1-1-.4-2.1-2.7-6-3.1-8.6-1-2.5 2-2.9 5.8-.9 8.4.2.3.2.7-.1.9-.3.3-.7.3-1 .1-3-2.7-3.4-7.4-.8-10.5.2-.2.6-.1.7.1.1.2 0 .4-.2.5z"/><path d="M7.7 17.5c-3.3-1.6-4.5-5.6-2.9-8.9 1.7-3.3 5.7-4.5 8.9-2.8 3.3 1.7 4.5 5.6 2.9 8.9-1.7 3.3-5.7 4.5-8.9 2.8zm1.2-3.3c.2 0 .5-.1.7-.3l.6-.3.7.3c.2.1.4 0 .6-.1.2-.2.2-.5.1-.7l-.2-.7.6-.5c.2-.2.3-.5.1-.7-.1-.2-.4-.3-.7-.2l-.7.2-.6-.5c-.2-.1-.5-.1-.7 0-.2.1-.3.4-.2.6l.2.7-.6.6c-.2.2-.2.5-.1.7.1.2.4.3.6.2l.7-.3.6.5c.2.1.4.1.5 0z"/></svg>
                微信登录
              </span>
              <span v-else class="btn-loading">
                <svg class="spinner" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="31.4 31.4" stroke-linecap="round"/></svg>
                登录中...
              </span>
            </button>

            <p class="sms-hint">开发环境：输入任意字符作为授权码即可登录</p>
          </div>

          <!-- Footer -->
          <div class="form-footer">
            <span class="footer-text">还没有账号？</span>
            <router-link to="/register" class="footer-link">立即注册</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { useUserStore } from '@/stores/user'
import { Lock, Message, ChatDotSquare } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const { login, loginBySms, loginByWechat, sendSmsCode, loading } = useAuth()

const activeTab = ref<'password' | 'sms' | 'wechat'>('password')
const showPassword = ref(false)
const rememberMe = ref(false)
const errorMsg = ref('')

const form = ref({
  phone: '',
  password: '',
  smsCode: '',
  wechatCode: '',
})

const smsSent = ref(false)
const smsDevCode = ref('')
const smsCountdown = ref(0)
const sendingSms = ref(false)
let countdownTimer: ReturnType<typeof setInterval> | null = null

// Registration success alert
const registerSuccess = ref(false)
const registerPhone = ref('')

const tabs = [
  { key: 'password' as const, label: '密码', icon: Lock },
  { key: 'sms' as const, label: '短信', icon: Message },
  { key: 'wechat' as const, label: '微信', icon: ChatDotSquare },
]

onMounted(() => {
  if (userStore.isLoggedIn) {
    const redirect = route.query.redirect as string
    router.replace(redirect || '/')
    return
  }
  // Show registration success alert when redirected from register page
  const registered = route.query.registered as string
  if (registered) {
    registerSuccess.value = true
    registerPhone.value = registered
    form.value.phone = registered !== '微信用户' ? registered : ''
  }
})

onUnmounted(() => {
  if (countdownTimer) clearInterval(countdownTimer)
})

function switchTab(key: 'password' | 'sms' | 'wechat') {
  activeTab.value = key
  errorMsg.value = ''
  smsSent.value = false
}

async function handlePasswordSubmit() {
  errorMsg.value = ''
  if (!form.value.phone) { errorMsg.value = '请输入手机号'; return }
  if (!form.value.password) { errorMsg.value = '请输入密码'; return }
  if (form.value.password.length < 6) { errorMsg.value = '密码长度至少6位'; return }

  try {
    await login(form.value.phone, form.value.password)
    if (rememberMe.value) {
      localStorage.setItem('remembered_phone', form.value.phone)
    } else {
      localStorage.removeItem('remembered_phone')
    }
    redirectAfterLogin()
  } catch (err: any) {
    if (err?.code === 'ECONNABORTED' || err?.code === 'ERR_NETWORK') {
      errorMsg.value = '网络连接失败，请确认后端服务已启动'
    } else {
      errorMsg.value = err?.response?.data?.detail || err?.message || '登录失败，请重试'
    }
  }
}

async function handleSendSms() {
  errorMsg.value = ''
  if (!form.value.phone) { errorMsg.value = '请输入手机号'; return }
  if (!/^1\d{10}$/.test(form.value.phone)) { errorMsg.value = '请输入正确的手机号'; return }

  sendingSms.value = true
  try {
    const result = await sendSmsCode(form.value.phone)
    smsSent.value = true
    smsDevCode.value = result?.code || ''
    smsCountdown.value = 60
    countdownTimer = setInterval(() => {
      smsCountdown.value--
      if (smsCountdown.value <= 0 && countdownTimer) {
        clearInterval(countdownTimer)
      }
    }, 1000)
  } catch (err: any) {
    if (err?.code === 'ECONNABORTED' || err?.code === 'ERR_NETWORK') {
      errorMsg.value = '网络连接失败，请确认后端服务已启动'
    } else {
      errorMsg.value = err?.response?.data?.detail || '发送验证码失败'
    }
  } finally {
    sendingSms.value = false
  }
}

async function handleSmsSubmit() {
  errorMsg.value = ''
  if (!form.value.phone) { errorMsg.value = '请输入手机号'; return }
  if (!form.value.smsCode) { errorMsg.value = '请输入验证码'; return }

  try {
    await loginBySms(form.value.phone, form.value.smsCode)
    redirectAfterLogin()
  } catch (err: any) {
    if (err?.code === 'ECONNABORTED' || err?.code === 'ERR_NETWORK') {
      errorMsg.value = '网络连接失败，请确认后端服务已启动'
    } else {
      errorMsg.value = err?.response?.data?.detail || '验证失败，请重试'
    }
  }
}

async function handleWechatSubmit() {
  errorMsg.value = ''
  if (!form.value.wechatCode) { errorMsg.value = '请输入授权码'; return }

  try {
    await loginByWechat(form.value.wechatCode)
    redirectAfterLogin()
  } catch (err: any) {
    if (err?.code === 'ECONNABORTED' || err?.code === 'ERR_NETWORK') {
      errorMsg.value = '网络连接失败，请确认后端服务已启动'
    } else {
      errorMsg.value = err?.response?.data?.detail || '微信登录失败，请重试'
    }
  }
}

function handleForgotPassword() {
  errorMsg.value = '请联系客服重置密码'
}

function redirectAfterLogin() {
  const redirect = route.query.redirect as string
  router.replace(redirect || '/')
}
</script>

<style scoped lang="scss">
// ============================================
// Design Tokens
// ============================================
$bg-deep: #0a0e1a;
$bg-card: #111827;
$bg-input: #1a2235;
$brand-amber: #f59e0b;
$brand-amber-light: #fbbf24;
$brand-amber-dark: #d97706;
$text-primary: #f1f5f9;
$text-secondary: #94a3b8;
$text-muted: #64748b;
$border-color: #1e293b;
$border-focus: #334155;
$danger: #ef4444;
$danger-bg: rgba(239, 68, 68, 0.1);
$success: #10b981;
$success-bg: rgba(16, 185, 129, 0.1);
$wechat-green: #07C160;

// ============================================
// Page Layout
// ============================================
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: $bg-deep;
  position: relative;
  overflow: hidden;
  font-family: 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', -apple-system, sans-serif;
}

// ============================================
// Background Layer
// ============================================
.bg-layer {
  position: absolute;
  inset: 0;
  overflow: hidden;
  z-index: 0;
}

.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.08;

  &.orb-1 {
    width: 600px; height: 600px;
    background: #3b82f6;
    top: -200px; right: -100px;
    animation: orb-drift 25s ease-in-out infinite;
  }
  &.orb-2 {
    width: 500px; height: 500px;
    background: #f59e0b;
    bottom: -150px; left: -150px;
    animation: orb-drift 30s ease-in-out infinite reverse;
  }
  &.orb-3 {
    width: 400px; height: 400px;
    background: #8b5cf6;
    top: 40%; left: 50%;
    animation: orb-drift 20s ease-in-out infinite;
  }
}

@keyframes orb-drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(40px, -30px) scale(1.08); }
  66% { transform: translate(-30px, 25px) scale(0.94); }
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
  background-size: 60px 60px;
}

// ============================================
// Auth Card
// ============================================
.auth-card {
  position: relative;
  z-index: 1;
  display: flex;
  max-width: 1040px;
  width: 100%;
  min-height: 640px;
  background: $bg-card;
  border-radius: 20px;
  overflow: hidden;
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.06),
    0 25px 60px -12px rgba(0,0,0,0.5),
    0 0 80px -20px rgba(59, 130, 246, 0.15);
}

// ============================================
// Brand Panel (Left)
// ============================================
.brand-panel {
  flex: 1.05;
  background: linear-gradient(160deg, #0f172a 0%, #1a2744 40%, #0f172a 100%);
  display: flex;
  align-items: center;
  padding: 56px 52px;
  position: relative;
  overflow: hidden;

  &::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 1px;
    height: 100%;
    background: linear-gradient(180deg, transparent, rgba(255,255,255,0.08), transparent);
  }
}

.brand-glow {
  position: absolute;
  top: 10%;
  left: -20%;
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(245, 158, 11, 0.12) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.brand-content {
  position: relative;
  z-index: 1;
  width: 100%;
}

// Logo
.brand-logo {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 56px;
  cursor: pointer;
  user-select: none;
}

.logo-mark {
  width: 44px; height: 44px;
  background: linear-gradient(135deg, $brand-amber, $brand-amber-dark);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0f172a;
  flex-shrink: 0;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-cn {
  font-size: 22px;
  font-weight: 800;
  color: $text-primary;
  line-height: 1.1;
  letter-spacing: 2px;
}

.logo-en {
  font-size: 9px;
  font-weight: 600;
  color: $text-muted;
  letter-spacing: 3px;
}

// Hero
.brand-hero {
  margin-bottom: 48px;
}

.hero-title {
  font-size: 32px;
  font-weight: 700;
  color: $text-primary;
  line-height: 1.35;
  margin-bottom: 16px;
}

.hero-line {
  display: block;
}

.hero-accent {
  background: linear-gradient(135deg, $brand-amber-light, $brand-amber);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 15px;
  color: $text-secondary;
  line-height: 1.7;
  max-width: 340px;
}

// Stats
.brand-stats {
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 48px;
  padding: 20px 0;
  border-top: 1px solid rgba(255,255,255,0.06);
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.stat-num {
  font-size: 22px;
  font-weight: 700;
  color: $brand-amber;
  letter-spacing: -0.5px;
}

.stat-label {
  font-size: 11px;
  color: $text-muted;
  letter-spacing: 0.5px;
}

.stat-divider {
  width: 1px;
  height: 32px;
  background: rgba(255,255,255,0.08);
  margin: 0 8px;
}

// Quote
.brand-quote {
  position: relative;
}

.quote-mark {
  width: 24px; height: 24px;
  color: $brand-amber;
  margin-bottom: 8px;
}

.brand-quote p {
  font-size: 14px;
  color: $text-secondary;
  line-height: 1.7;
  font-style: italic;
  margin-bottom: 16px;
}

.quote-author {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-avatar {
  width: 36px; height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, $brand-amber, $brand-amber-dark);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
  flex-shrink: 0;
}

.author-name {
  display: block;
  font-size: 13px;
  color: $text-primary;
  font-weight: 500;
}

.author-role {
  display: block;
  font-size: 11px;
  color: $text-muted;
}

// ============================================
// Form Panel (Right)
// ============================================
.form-panel {
  flex: 0.95;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 52px;
}

.form-container {
  width: 100%;
  max-width: 380px;
}

.form-header {
  margin-bottom: 32px;
}

.form-title {
  font-size: 26px;
  font-weight: 700;
  color: $text-primary;
  margin-bottom: 6px;
}

.form-subtitle {
  font-size: 14px;
  color: $text-muted;
}

// ============================================
// Tab Switcher
// ============================================
.auth-tabs {
  display: flex;
  position: relative;
  background: $bg-input;
  border-radius: 12px;
  padding: 4px;
  margin-bottom: 28px;
}

.tab-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 8px;
  border: none;
  background: transparent;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  color: $text-muted;
  cursor: pointer;
  position: relative;
  z-index: 1;
  transition: color 0.3s ease;
  font-family: inherit;

  &:hover { color: $text-secondary; }

  &.active {
    color: $text-primary;
  }
}

.tab-icon {
  display: flex;
  align-items: center;
}

.tab-indicator {
  position: absolute;
  top: 4px;
  left: 4px;
  width: calc((100% - 8px) / 3);
  height: calc(100% - 8px);
  background: $border-color;
  border-radius: 10px;
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

// ============================================
// Alerts
// ============================================
.alert {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  border-radius: 10px;
  margin-bottom: 20px;
  font-size: 13px;
  line-height: 1.5;

  &-error {
    background: $danger-bg;
    color: $danger;
    border: 1px solid rgba(239, 68, 68, 0.2);
  }

  &-success {
    background: $success-bg;
    color: $success;
    border: 1px solid rgba(16, 185, 129, 0.2);
  }
}

.alert-icon {
  width: 18px; height: 18px;
  flex-shrink: 0;
  margin-top: 1px;
}

.alert-title {
  font-weight: 600;
  margin-bottom: 2px;
}

.alert-desc {
  opacity: 0.85;
  font-size: 12px;
}

.alert-close {
  flex-shrink: 0;
  width: 20px; height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: none;
  color: inherit;
  opacity: 0.5;
  cursor: pointer;
  border-radius: 4px;
  padding: 0;
  margin-top: 1px;
  transition: opacity 0.2s;

  &:hover { opacity: 1; }

  svg {
    width: 14px; height: 14px;
  }
}

.alert-enter-active,
.alert-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.alert-enter-from,
.alert-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

// ============================================
// Form Elements
// ============================================
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.input-group {
  margin-bottom: 18px;
}

.input-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: $text-secondary;
  margin-bottom: 6px;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: $bg-input;
  border-radius: 10px;
  border: 1.5px solid transparent;
  transition: all 0.25s ease;
  overflow: hidden;

  &:focus-within {
    border-color: $brand-amber;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.08);
  }
}

.input-prefix {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-left: 14px;
  color: $text-muted;
  flex-shrink: 0;

  svg {
    width: 18px; height: 18px;
  }
}

.input-suffix {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-right: 14px;
  color: $text-muted;
  background: none;
  border: none;
  cursor: pointer;
  flex-shrink: 0;
  transition: color 0.2s;

  &:hover { color: $text-secondary; }

  svg {
    width: 18px; height: 18px;
  }
}

.input-field {
  flex: 1;
  width: 100%;
  padding: 13px 12px;
  background: transparent;
  border: none;
  outline: none;
  font-size: 15px;
  color: $text-primary;
  font-family: inherit;

  &::placeholder {
    color: $text-muted;
    font-size: 14px;
  }

  // Autofill override
  &:-webkit-autofill,
  &:-webkit-autofill:hover,
  &:-webkit-autofill:focus {
    -webkit-text-fill-color: $text-primary;
    -webkit-box-shadow: 0 0 0px 1000px $bg-input inset;
    transition: background-color 5000s ease-in-out 0s;
  }
}

// Form extras
.form-extra {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 13px;
  color: $text-muted;
  user-select: none;

  input[type="checkbox"] {
    display: none;
  }

  .checkmark {
    width: 18px; height: 18px;
    border-radius: 5px;
    border: 1.5px solid $border-focus;
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    position: relative;

    &::after {
      content: '';
      position: absolute;
      width: 5px; height: 9px;
      border: solid white;
      border-width: 0 2px 2px 0;
      transform: rotate(45deg) scale(0);
      transition: transform 0.15s ease;
      margin-top: -1px;
    }
  }

  input:checked + .checkmark {
    background: $brand-amber;
    border-color: $brand-amber;

    &::after {
      transform: rotate(45deg) scale(1);
    }
  }
}

.forgot-link {
  font-size: 13px;
  color: $brand-amber;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.2s;

  &:hover { color: $brand-amber-light; }
}

// ============================================
// Submit Button
// ============================================
.submit-btn {
  width: 100%;
  padding: 14px 0;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 2px;
  cursor: pointer;
  color: #0f172a;
  background: linear-gradient(135deg, $brand-amber-light, $brand-amber);
  box-shadow: 0 4px 16px rgba(245, 158, 11, 0.25);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: inherit;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, $brand-amber, $brand-amber-dark);
    opacity: 0;
    transition: opacity 0.3s;
  }

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 6px 24px rgba(245, 158, 11, 0.35);

    &::before { opacity: 1; }
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  > span {
    position: relative;
    z-index: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
}

.wechat-btn {
  background: linear-gradient(135deg, #2dd46e, $wechat-green) !important;
  box-shadow: 0 4px 16px rgba(7, 193, 96, 0.25) !important;
  color: #fff !important;

  &::before {
    background: linear-gradient(135deg, $wechat-green, #059648) !important;
  }

  &:hover:not(:disabled) {
    box-shadow: 0 6px 24px rgba(7, 193, 96, 0.35) !important;
  }
}

.wechat-logo {
  width: 20px; height: 20px;
  vertical-align: middle;
}

// Loading spinner
.spinner {
  width: 20px; height: 20px;
  animation: spin 0.8s linear infinite;

  &.sm { width: 16px; height: 16px; }

  circle { stroke-dashoffset: 0; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.btn-loading {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

// ============================================
// SMS Specific
// ============================================
.sms-row {
  display: flex;
  gap: 10px;
}

.sms-input-wrap {
  flex: 1;
}

.sms-btn {
  flex-shrink: 0;
  min-width: 115px;
  padding: 0 12px;
  border-radius: 10px;
  border: 1.5px solid $border-focus;
  background: transparent;
  color: $brand-amber;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.25s ease;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover:not(:disabled) {
    border-color: $brand-amber;
    background: rgba(245, 158, 11, 0.06);
  }

  &:disabled {
    color: $text-muted;
    border-color: $border-color;
    cursor: not-allowed;
  }
}

.sms-hint {
  text-align: center;
  margin-top: 16px;
  font-size: 12px;
  color: $text-muted;
  line-height: 1.6;
}

// ============================================
// WeChat Specific
// ============================================
.wechat-qr {
  margin-bottom: 4px;
}

.qr-wrapper {
  display: flex;
  justify-content: center;
}

.qr-placeholder {
  width: 160px; height: 160px;
  background: $bg-input;
  border: 2px dashed $border-focus;
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: $text-muted;
  transition: all 0.3s;

  &:hover {
    border-color: $wechat-green;
    color: $wechat-green;
  }

  p {
    font-size: 12px;
  }
}

.qr-icon {
  width: 48px; height: 48px;
}

// Divider
.divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 20px 0;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: $border-color;
}

.divider-text {
  font-size: 12px;
  color: $text-muted;
  white-space: nowrap;
}

// ============================================
// Form Footer
// ============================================
.form-footer {
  text-align: center;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid $border-color;
}

.footer-text {
  font-size: 14px;
  color: $text-muted;
  margin-right: 4px;
}

.footer-link {
  font-size: 14px;
  font-weight: 600;
  color: $brand-amber;
  text-decoration: none;
  transition: color 0.2s;

  &:hover { color: $brand-amber-light; }
}

// ============================================
// Responsive
// ============================================
@media (max-width: 768px) {
  .auth-page {
    padding: 0;
    align-items: flex-start;
  }

  .auth-card {
    flex-direction: column;
    border-radius: 0;
    min-height: 100vh;
  }

  .brand-panel {
    display: none;
  }

  .form-panel {
    padding: 40px 28px;
  }

  .form-container {
    max-width: 100%;
  }
}
</style>
