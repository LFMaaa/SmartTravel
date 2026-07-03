<template>
  <div class="auth-page">
    <!-- Decorative background -->
    <div class="bg-layer">
      <div class="bg-orb orb-1"></div>
      <div class="bg-orb orb-2"></div>
    </div>

    <div class="auth-card">
      <!-- Left: Brand Panel -->
      <div class="brand-panel">
        <div class="brand-content">
          <div class="brand-logo" @click="$router.push('/')">
            <span class="brand-icon">🌿</span>
            <div class="brand-text">
              <span class="brand-name">旅游AI</span>
              <span class="brand-en">SmartTravel</span>
            </div>
          </div>

          <div class="brand-hero">
            <h2 class="hero-title">
              <span>探索世界，</span>
              <span class="hero-accent">随心而行</span>
            </h2>
            <p>AI 驱动的智能行程规划，让每一次出发都成为难忘的旅程</p>
          </div>

          <div class="brand-stats">
            <div class="stat-item">
              <span class="stat-num">50+</span>
              <span class="stat-label">目的地覆盖</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-num">10万+</span>
              <span class="stat-label">行程已生成</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-num">98%</span>
              <span class="stat-label">好评率</span>
            </div>
          </div>

          <div class="brand-quote">
            <span class="quote-mark">"</span>
            <p>这是我用过最智能的旅行规划工具，AI 生成的行程完全超出了我的预期。</p>
            <div class="quote-author">
              <div class="author-avatar">李</div>
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
          <div class="form-header">
            <h3>欢迎回来</h3>
            <p>选择你喜欢的方式登录</p>
          </div>

          <!-- Tab Switcher -->
          <div class="auth-tabs">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              :class="['tab-item', { active: activeTab === tab.key }]"
              @click="switchTab(tab.key)"
            >
              <el-icon :size="16"><component :is="tab.icon" /></el-icon>
              <span>{{ tab.label }}</span>
            </button>
            <div class="tab-indicator" :style="{ transform: `translateX(${tabs.findIndex(t => t.key === activeTab) * 100}%)` }"></div>
          </div>

          <!-- Error Alert -->
          <transition name="alert">
            <div v-if="errorMsg" class="alert alert-error">
              <svg viewBox="0 0 20 20" fill="currentColor" class="alert-icon"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>
              <span>{{ errorMsg }}</span>
              <button class="alert-close" @click="errorMsg = ''">×</button>
            </div>
          </transition>

          <!-- SMS Sent Success -->
          <transition name="alert">
            <div v-if="smsSent" class="alert alert-success">
              <svg viewBox="0 0 20 20" fill="currentColor" class="alert-icon"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
              <div>
                <p class="alert-title">验证码已发送</p>
                <p class="alert-desc">已发送至 {{ form.phone }}，有效期5分钟<span v-if="smsDevCode">（开发：{{ smsDevCode }}）</span></p>
              </div>
              <button class="alert-close" @click="smsSent = false">×</button>
            </div>
          </transition>

          <!-- Registration Success -->
          <transition name="alert">
            <div v-if="registerSuccess" class="alert alert-success">
              <svg viewBox="0 0 20 20" fill="currentColor" class="alert-icon"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
              <div>
                <p class="alert-title">注册成功</p>
                <p class="alert-desc">账号 {{ registerPhone }} 已创建，请登录</p>
              </div>
              <button class="alert-close" @click="registerSuccess = false">×</button>
            </div>
          </transition>

          <!-- Password Login -->
          <form v-if="activeTab === 'password'" class="auth-form" @submit.prevent="handlePasswordSubmit">
            <div class="input-group">
              <label class="input-label">手机号</label>
              <div class="input-wrapper">
                <span class="input-prefix">📱</span>
                <input v-model="form.phone" type="tel" class="input-field" placeholder="请输入手机号" maxlength="11" />
              </div>
            </div>
            <div class="input-group">
              <label class="input-label">密码</label>
              <div class="input-wrapper">
                <span class="input-prefix">🔒</span>
                <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="input-field" placeholder="请输入密码" />
                <button type="button" class="input-suffix" @click="showPassword = !showPassword">
                  {{ showPassword ? '🙈' : '👁️' }}
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
              <span v-else class="btn-loading">登录中...</span>
            </button>
          </form>

          <!-- SMS Login -->
          <form v-if="activeTab === 'sms'" class="auth-form" @submit.prevent="handleSmsSubmit">
            <div class="input-group">
              <label class="input-label">手机号</label>
              <div class="input-wrapper">
                <span class="input-prefix">📱</span>
                <input v-model="form.phone" type="tel" class="input-field" placeholder="请输入手机号" maxlength="11" />
              </div>
            </div>
            <div class="input-group">
              <label class="input-label">验证码</label>
              <div class="sms-row">
                <div class="input-wrapper sms-input-wrap">
                  <span class="input-prefix">💬</span>
                  <input v-model="form.smsCode" type="text" class="input-field" placeholder="输入6位验证码" maxlength="6" />
                </div>
                <button type="button" class="sms-btn" :disabled="smsCountdown > 0 || sendingSms" @click="handleSendSms">
                  <span v-if="sendingSms">发送中...</span>
                  <span v-else-if="smsCountdown > 0">{{ smsCountdown }}s 后重试</span>
                  <span v-else>获取验证码</span>
                </button>
              </div>
            </div>
            <button type="submit" class="submit-btn" :disabled="loading">
              <span v-if="!loading">登录 / 注册</span>
              <span v-else class="btn-loading">验证中...</span>
            </button>
            <p class="sms-hint">未注册手机号将自动创建账号</p>
          </form>

          <!-- WeChat Login -->
          <div v-if="activeTab === 'wechat'" class="auth-form">
            <div class="wechat-qr">
              <div class="qr-placeholder">
                <div class="qr-icon">📱</div>
                <p>请使用微信扫一扫</p>
              </div>
            </div>
            <div class="divider"><span class="divider-line"></span><span class="divider-text">或使用授权码登录</span><span class="divider-line"></span></div>
            <div class="input-group">
              <label class="input-label">微信授权码</label>
              <div class="input-wrapper">
                <span class="input-prefix">💚</span>
                <input v-model="form.wechatCode" type="text" class="input-field" placeholder="输入授权码（开发环境任意字符）" />
              </div>
            </div>
            <button type="button" class="submit-btn wechat-btn" :disabled="loading" @click="handleWechatSubmit">
              <span v-if="!loading">微信登录</span>
              <span v-else class="btn-loading">登录中...</span>
            </button>
            <p class="sms-hint">开发环境：输入任意字符作为授权码即可登录</p>
          </div>

          <div class="form-footer">
            <span>还没有账号？</span>
            <router-link to="/register">立即注册</router-link>
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

const form = ref({ phone: '', password: '', smsCode: '', wechatCode: '' })

const smsSent = ref(false)
const smsDevCode = ref('')
const smsCountdown = ref(0)
const sendingSms = ref(false)
let countdownTimer: ReturnType<typeof setInterval> | null = null

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
  const registered = route.query.registered as string
  if (registered) {
    registerSuccess.value = true
    registerPhone.value = registered
    form.value.phone = registered !== '微信用户' ? registered : ''
  }
})

onUnmounted(() => { if (countdownTimer) clearInterval(countdownTimer) })

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
    if (rememberMe.value) localStorage.setItem('remembered_phone', form.value.phone)
    else localStorage.removeItem('remembered_phone')
    redirectAfterLogin()
  } catch (err: any) {
    errorMsg.value = err?.response?.data?.detail || err?.message || '登录失败，请重试'
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
    countdownTimer = setInterval(() => { smsCountdown.value--; if (smsCountdown.value <= 0 && countdownTimer) clearInterval(countdownTimer) }, 1000)
  } catch (err: any) {
    errorMsg.value = err?.response?.data?.detail || '发送验证码失败'
  } finally { sendingSms.value = false }
}

async function handleSmsSubmit() {
  errorMsg.value = ''
  if (!form.value.phone) { errorMsg.value = '请输入手机号'; return }
  if (!form.value.smsCode) { errorMsg.value = '请输入验证码'; return }
  try { await loginBySms(form.value.phone, form.value.smsCode); redirectAfterLogin() }
  catch (err: any) { errorMsg.value = err?.response?.data?.detail || '验证失败，请重试' }
}

async function handleWechatSubmit() {
  errorMsg.value = ''
  if (!form.value.wechatCode) { errorMsg.value = '请输入授权码'; return }
  try { await loginByWechat(form.value.wechatCode); redirectAfterLogin() }
  catch (err: any) { errorMsg.value = err?.response?.data?.detail || '微信登录失败，请重试' }
}

function handleForgotPassword() { errorMsg.value = '请联系客服重置密码' }
function redirectAfterLogin() { const redirect = route.query.redirect as string; router.replace(redirect || '/') }
</script>

<style scoped lang="scss">
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
$danger: #D4756B;
$success: #8FAF8A;

.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: $bg-warm;
  position: relative;
  overflow: hidden;
  font-family: 'Noto Sans SC', 'PingFang SC', sans-serif;
}

.bg-layer { position: absolute; inset: 0; overflow: hidden; z-index: 0; }
.bg-orb {
  position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.1;
  &.orb-1 { width: 500px; height: 500px; background: rgba(184, 196, 184, 0.4); top: -150px; right: -100px; }
  &.orb-2 { width: 400px; height: 400px; background: rgba(232, 213, 208, 0.5); bottom: -100px; left: -80px; }
}

.auth-card {
  position: relative; z-index: 1;
  display: flex; max-width: 960px; width: 100%; min-height: 600px;
  background: $bg-white; border-radius: 24px; overflow: hidden;
  box-shadow: 0 8px 40px rgba(166, 139, 122, 0.12), 0 0 0 1px rgba(232, 213, 208, 0.3);
}

// Brand Panel
.brand-panel {
  flex: 1; background: linear-gradient(160deg, $bg-oat 0%, #F0EBE3 100%);
  display: flex; align-items: center; padding: 48px 44px; position: relative;
  &::after { content: ''; position: absolute; top: 0; right: 0; width: 1px; height: 100%; background: linear-gradient(180deg, transparent, rgba(166,139,122,0.15), transparent); }
}
.brand-content { position: relative; z-index: 1; width: 100%; }

.brand-logo { display: flex; align-items: center; gap: 14px; margin-bottom: 48px; cursor: pointer; }
.brand-icon { font-size: 36px; }
.brand-name { font-size: 22px; font-weight: 600; color: $text-primary; letter-spacing: 1px; display: block; }
.brand-en { font-size: 9px; color: $text-muted; letter-spacing: 2px; font-weight: 500; }

.brand-hero { margin-bottom: 40px; }
.brand-hero h2 { font-size: 28px; font-weight: 300; color: $text-primary; line-height: 1.4; margin-bottom: 14px; }
.brand-hero h2 .hero-accent { font-weight: 600; color: $brand-brown; }
.brand-hero p { font-size: 14px; color: $text-secondary; line-height: 1.7; }

.brand-stats { display: flex; align-items: center; gap: 0; margin-bottom: 40px; padding: 18px 0; border-top: 1px solid $border; border-bottom: 1px solid $border; }
.stat-item { display: flex; flex-direction: column; gap: 2px; flex: 1; }
.stat-num { font-size: 22px; font-weight: 700; color: $brand-brown; }
.stat-label { font-size: 11px; color: $text-secondary; }
.stat-divider { width: 1px; height: 32px; background: $border; margin: 0 8px; }

.brand-quote { position: relative; }
.quote-mark { font-size: 40px; color: $brand-brown; line-height: 1; font-family: serif; display: block; margin-bottom: 4px; }
.brand-quote p { font-size: 13px; color: $text-secondary; line-height: 1.7; font-style: italic; margin-bottom: 14px; }
.quote-author { display: flex; align-items: center; gap: 12px; }
.author-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, $brand-nude, $brand-sage); display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600; color: white; }
.author-name { display: block; font-size: 13px; color: $text-primary; font-weight: 500; }
.author-role { display: block; font-size: 11px; color: $text-secondary; }

// Form Panel
.form-panel { flex: 0.9; display: flex; align-items: center; justify-content: center; padding: 48px 44px; }
.form-container { width: 100%; max-width: 360px; }
.form-header { margin-bottom: 28px; }
.form-header h3 { font-size: 26px; font-weight: 600; color: $text-primary; margin-bottom: 6px; }
.form-header p { font-size: 14px; color: $text-muted; }

// Tabs
.auth-tabs { display: flex; position: relative; background: $bg-oat; border-radius: 12px; padding: 4px; margin-bottom: 24px; }
.tab-item { flex: 1; display: flex; align-items: center; justify-content: center; gap: 6px; padding: 10px 8px; border: none; background: transparent; border-radius: 10px; font-size: 13px; font-weight: 500; color: $text-muted; cursor: pointer; position: relative; z-index: 1; transition: color 0.3s; font-family: inherit; }
.tab-item:hover { color: $text-secondary; }
.tab-item.active { color: $brand-brown; }
.tab-indicator { position: absolute; top: 4px; left: 4px; width: calc((100% - 8px) / 3); height: calc(100% - 8px); background: $bg-white; border-radius: 10px; transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 1px 4px rgba(166,139,122,0.08); border: 1px solid $border; }

// Alerts
.alert { display: flex; align-items: flex-start; gap: 10px; padding: 12px 14px; border-radius: 10px; margin-bottom: 18px; font-size: 13px; line-height: 1.5; }
.alert-error { background: rgba(212,117,107,0.08); color: $danger; border: 1px solid rgba(212,117,107,0.2); }
.alert-success { background: rgba(143,175,138,0.08); color: $success; border: 1px solid rgba(143,175,138,0.2); }
.alert-icon { width: 18px; height: 18px; flex-shrink: 0; margin-top: 1px; }
.alert-title { font-weight: 600; margin-bottom: 2px; }
.alert-desc { opacity: 0.85; font-size: 12px; }
.alert-close { flex-shrink: 0; border: none; background: none; color: inherit; opacity: 0.5; cursor: pointer; font-size: 18px; padding: 0; line-height: 1; &:hover { opacity: 1; } }

// Form
.auth-form { display: flex; flex-direction: column; gap: 0; }
.input-group { margin-bottom: 16px; }
.input-label { display: block; font-size: 13px; font-weight: 500; color: $text-secondary; margin-bottom: 6px; }
.input-wrapper { display: flex; align-items: center; background: $bg-oat; border-radius: 10px; border: 1.5px solid transparent; transition: all 0.25s; overflow: hidden; }
.input-wrapper:focus-within { border-color: $brand-sage; box-shadow: 0 0 0 3px rgba(184,196,184,0.2); }
.input-prefix { padding-left: 14px; font-size: 16px; flex-shrink: 0; }
.input-suffix { padding-right: 14px; background: none; border: none; cursor: pointer; font-size: 16px; flex-shrink: 0; }
.input-field { flex: 1; padding: 13px 12px; background: transparent; border: none; outline: none; font-size: 15px; color: $text-primary; font-family: inherit; }
.input-field::placeholder { color: $text-muted; font-size: 14px; }

.form-extra { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
.remember-me { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 13px; color: $text-secondary; }
.remember-me input[type="checkbox"] { display: none; }
.checkmark { width: 18px; height: 18px; border-radius: 5px; border: 1.5px solid $border; background: transparent; display: flex; align-items: center; justify-content: center; transition: all 0.2s; position: relative; }
.checkmark::after { content: ''; position: absolute; width: 5px; height: 9px; border: solid white; border-width: 0 2px 2px 0; transform: rotate(45deg) scale(0); transition: transform 0.15s; margin-top: -1px; }
.remember-me input:checked + .checkmark { background: $brand-sage; border-color: $brand-sage; }
.remember-me input:checked + .checkmark::after { transform: rotate(45deg) scale(1); }
.forgot-link { font-size: 13px; color: $brand-brown; cursor: pointer; }

.submit-btn { width: 100%; padding: 14px 0; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; letter-spacing: 2px; cursor: pointer; color: white; background: linear-gradient(135deg, $brand-nude 0%, $brand-sage 100%); box-shadow: 0 4px 16px rgba(184,196,184,0.3); transition: all 0.3s; font-family: inherit; }
.submit-btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 6px 24px rgba(184,196,184,0.4); }
.submit-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.wechat-btn { background: linear-gradient(135deg, #7EC87E, #07C160) !important; }

// SMS
.sms-row { display: flex; gap: 10px; }
.sms-input-wrap { flex: 1; }
.sms-btn { flex-shrink: 0; min-width: 110px; padding: 0 12px; border-radius: 10px; border: 1.5px solid $border; background: transparent; color: $brand-brown; font-size: 13px; font-weight: 500; cursor: pointer; font-family: inherit; transition: all 0.25s; }
.sms-btn:hover:not(:disabled) { border-color: $brand-brown; background: rgba(166,139,122,0.08); }
.sms-btn:disabled { color: $text-muted; border-color: $border; cursor: not-allowed; }
.sms-hint { text-align: center; margin-top: 14px; font-size: 12px; color: $text-muted; }

// WeChat
.wechat-qr { margin-bottom: 4px; display: flex; justify-content: center; }
.qr-placeholder { width: 140px; height: 140px; background: $bg-oat; border: 2px dashed $border; border-radius: 14px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; color: $text-muted; transition: all 0.3s; }
.qr-placeholder:hover { border-color: $brand-sage; color: $brand-sage; }
.qr-icon { font-size: 36px; }
.qr-placeholder p { font-size: 12px; }
.divider { display: flex; align-items: center; gap: 12px; margin: 18px 0; }
.divider-line { flex: 1; height: 1px; background: $border; }
.divider-text { font-size: 12px; color: $text-muted; white-space: nowrap; }

// Footer
.form-footer { text-align: center; margin-top: 28px; padding-top: 22px; border-top: 1px solid $border; font-size: 14px; color: $text-secondary; }
.form-footer a { color: $brand-brown; font-weight: 600; margin-left: 4px; }

.btn-loading { display: inline-flex; align-items: center; gap: 8px; }

@media (max-width: 768px) {
  .auth-page { padding: 0; align-items: flex-start; }
  .auth-card { flex-direction: column; border-radius: 0; min-height: 100vh; }
  .brand-panel { display: none; }
  .form-panel { padding: 40px 28px; }
  .form-container { max-width: 100%; }
}
</style>
