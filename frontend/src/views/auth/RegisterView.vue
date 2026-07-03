<template>
  <div class="auth-page">
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
            <h2>开启你的<span class="hero-accent">智能旅行</span></h2>
            <p>创建账号，体验 AI 驱动的个性化行程规划服务</p>
          </div>

          <div class="register-steps">
            <div class="step-item">
              <div class="step-num">01</div>
              <div class="step-info"><span class="step-title">填写信息</span><span class="step-desc">输入手机号和密码</span></div>
            </div>
            <div class="step-connector"></div>
            <div class="step-item">
              <div class="step-num">02</div>
              <div class="step-info"><span class="step-title">验证身份</span><span class="step-desc">短信验证码确认</span></div>
            </div>
            <div class="step-connector"></div>
            <div class="step-item">
              <div class="step-num">03</div>
              <div class="step-info"><span class="step-title">开始探索</span><span class="step-desc">生成你的第一份行程</span></div>
            </div>
          </div>

          <div class="brand-quote">
            <span class="quote-mark">"</span>
            <p>注册智游后，我十分钟就搞定了原本要花几天规划的日本行程，太神奇了。</p>
            <div class="quote-author">
              <div class="author-avatar">王</div>
              <div><span class="author-name">旅行者小王</span><span class="author-role">智游年度会员</span></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Form Panel -->
      <div class="form-panel">
        <div class="form-container">
          <div class="form-header">
            <h3>创建账号</h3>
            <p>注册智游，开启智能旅行体验</p>
          </div>

          <!-- Tab Switcher -->
          <div class="auth-tabs">
            <button v-for="tab in tabs" :key="tab.key" :class="['tab-item', { active: activeTab === tab.key }]" @click="switchTab(tab.key)">
              <el-icon :size="16"><component :is="tab.icon" /></el-icon>
              <span>{{ tab.label }}</span>
            </button>
            <div class="tab-indicator" :style="{ transform: `translateX(${tabs.findIndex(t => t.key === activeTab) * 100}%)` }"></div>
          </div>

          <!-- Error Alert -->
          <transition name="alert">
            <div v-if="errorMsg" class="alert alert-error">
              <svg viewBox="0 0 20 20" fill="currentColor" class="alert-icon"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>
              <div>
                <span>{{ errorMsg }}</span>
                <router-link v-if="alreadyRegistered" :to="`/login?registered=${form.phone}`" class="alert-link">去登录 →</router-link>
              </div>
              <button class="alert-close" @click="errorMsg = ''; alreadyRegistered = false">×</button>
            </div>
          </transition>

          <!-- SMS Sent -->
          <transition name="alert">
            <div v-if="smsSent" class="alert alert-success">
              <svg viewBox="0 0 20 20" fill="currentColor" class="alert-icon"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
              <div><p class="alert-title">验证码已发送</p><p class="alert-desc">已发送至 {{ form.phone }}<span v-if="smsDevCode">（开发：{{ smsDevCode }}）</span></p></div>
              <button class="alert-close" @click="smsSent = false">×</button>
            </div>
          </transition>

          <!-- Password Register -->
          <form v-if="activeTab === 'password'" class="auth-form" @submit.prevent="handlePasswordRegister">
            <div class="input-group">
              <label class="input-label">手机号</label>
              <div class="input-wrapper">
                <span class="input-prefix">📱</span>
                <input v-model="form.phone" type="tel" class="input-field" placeholder="请输入手机号" maxlength="11" />
              </div>
            </div>

            <div class="input-group">
              <label class="input-label">昵称（选填）</label>
              <div class="input-wrapper">
                <span class="input-prefix">👤</span>
                <input v-model="form.nickname" type="text" class="input-field" placeholder="给自己起个名字" />
              </div>
            </div>

            <div class="input-group">
              <label class="input-label">设置密码</label>
              <div class="input-wrapper">
                <span class="input-prefix">🔒</span>
                <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="input-field" placeholder="至少6位密码" />
                <button type="button" class="input-suffix" @click="showPassword = !showPassword">{{ showPassword ? '🙈' : '👁️' }}</button>
              </div>
            </div>

            <div class="input-group">
              <label class="input-label">确认密码</label>
              <div class="input-wrapper">
                <span class="input-prefix">🔒</span>
                <input v-model="confirmPassword" :type="showPassword ? 'text' : 'password'" class="input-field" placeholder="请再次输入密码" />
              </div>
            </div>

            <!-- Password Strength -->
            <div v-if="form.password" class="password-strength">
              <div class="strength-bars">
                <div :class="['strength-bar', { active: strengthLevel >= 1, weak: strengthLevel === 1, medium: strengthLevel === 2, strong: strengthLevel >= 3 }]"></div>
                <div :class="['strength-bar', { active: strengthLevel >= 2, medium: strengthLevel === 2, strong: strengthLevel >= 3 }]"></div>
                <div :class="['strength-bar', { active: strengthLevel >= 3, strong: strengthLevel >= 3 }]"></div>
              </div>
              <span class="strength-text" :class="strengthClass">{{ strengthLabel }}</span>
            </div>

            <div class="agreement-row">
              <label class="remember-me">
                <input type="checkbox" v-model="agreedToTerms" />
                <span class="checkmark"></span>
                <span>我已阅读并同意</span>
              </label>
              <a class="forgot-link" @click.prevent="showTerms">《用户协议》</a>
            </div>

            <button type="submit" class="submit-btn" :disabled="loading || !agreedToTerms">
              <span v-if="!loading">注 册</span>
              <span v-else class="btn-loading">注册中...</span>
            </button>
          </form>

          <!-- SMS Register -->
          <form v-if="activeTab === 'sms'" class="auth-form" @submit.prevent="handleSmsRegister">
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
                  <span v-else-if="smsCountdown > 0">{{ smsCountdown }}s</span>
                  <span v-else>获取验证码</span>
                </button>
              </div>
            </div>
            <div class="input-group">
              <label class="input-label">昵称（选填）</label>
              <div class="input-wrapper">
                <span class="input-prefix">👤</span>
                <input v-model="form.nickname" type="text" class="input-field" placeholder="给自己起个名字" />
              </div>
            </div>
            <button type="submit" class="submit-btn" :disabled="loading">
              <span v-if="!loading">注册 / 登录</span>
              <span v-else class="btn-loading">验证中...</span>
            </button>
            <p class="sms-hint">未注册手机号将自动创建账号</p>
          </form>

          <!-- WeChat Register -->
          <div v-if="activeTab === 'wechat'" class="auth-form">
            <div class="wechat-qr">
              <div class="qr-placeholder"><div class="qr-icon">📱</div><p>请使用微信扫一扫</p></div>
            </div>
            <div class="divider"><span class="divider-line"></span><span class="divider-text">或使用授权码注册</span><span class="divider-line"></span></div>
            <div class="input-group">
              <label class="input-label">微信授权码</label>
              <div class="input-wrapper">
                <span class="input-prefix">💚</span>
                <input v-model="form.wechatCode" type="text" class="input-field" placeholder="输入授权码（开发环境任意字符）" />
              </div>
            </div>
            <div class="input-group">
              <label class="input-label">昵称（选填）</label>
              <div class="input-wrapper">
                <span class="input-prefix">👤</span>
                <input v-model="form.nickname" type="text" class="input-field" placeholder="给自己起个名字" />
              </div>
            </div>
            <button type="button" class="submit-btn wechat-btn" :disabled="loading" @click="handleWechatRegister">
              <span v-if="!loading">微信注册</span>
              <span v-else class="btn-loading">注册中...</span>
            </button>
            <p class="sms-hint">开发环境：输入任意字符作为授权码即可注册</p>
          </div>

          <div class="form-footer">
            <span>已有账号？</span>
            <router-link to="/login">立即登录</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { useUserStore } from '@/stores/user'
import { Lock, Message, ChatDotSquare } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const { register, sendSmsCode, loginBySms, loginByWechat, loading } = useAuth()

const activeTab = ref<'password' | 'sms' | 'wechat'>('password')
const showPassword = ref(false)
const agreedToTerms = ref(false)
const confirmPassword = ref('')
const errorMsg = ref('')
const alreadyRegistered = ref(false)

const form = ref({ phone: '', password: '', nickname: '', smsCode: '', wechatCode: '' })

const smsSent = ref(false)
const smsDevCode = ref('')
const smsCountdown = ref(0)
const sendingSms = ref(false)
let countdownTimer: ReturnType<typeof setInterval> | null = null

const tabs = [
  { key: 'password' as const, label: '密码', icon: Lock },
  { key: 'sms' as const, label: '短信', icon: Message },
  { key: 'wechat' as const, label: '微信', icon: ChatDotSquare },
]

onMounted(() => { if (userStore.isLoggedIn) router.replace('/') })
onUnmounted(() => { if (countdownTimer) clearInterval(countdownTimer) })

const strengthLevel = computed(() => {
  const pwd = form.value.password
  if (!pwd) return 0
  let score = 0
  if (pwd.length >= 6) score++
  if (pwd.length >= 10) score++
  if (/[A-Z]/.test(pwd) && /[a-z]/.test(pwd)) score++
  if (/\d/.test(pwd)) score++
  if (/[!@#$%^&*(),.?":{}|<>]/.test(pwd)) score++
  return Math.min(3, score)
})
const strengthLabel = computed(() => ['', '较弱', '中等', '强'][strengthLevel.value] || '')
const strengthClass = computed(() => {
  if (strengthLevel.value <= 1) return 'text-weak'
  if (strengthLevel.value === 2) return 'text-medium'
  return 'text-strong'
})

function switchTab(key: 'password' | 'sms' | 'wechat') { activeTab.value = key; errorMsg.value = ''; alreadyRegistered.value = false; smsSent.value = false }

async function handleSendSms() {
  errorMsg.value = ''
  if (!form.value.phone) { errorMsg.value = '请输入手机号'; return }
  if (!/^1\d{10}$/.test(form.value.phone)) { errorMsg.value = '请输入正确的手机号'; return }
  sendingSms.value = true
  try {
    const result = await sendSmsCode(form.value.phone)
    smsSent.value = true; smsDevCode.value = result?.code || ''; smsCountdown.value = 60
    countdownTimer = setInterval(() => { smsCountdown.value--; if (smsCountdown.value <= 0 && countdownTimer) clearInterval(countdownTimer) }, 1000)
  } catch (err: any) { errorMsg.value = err?.response?.data?.detail || '发送验证码失败' }
  finally { sendingSms.value = false }
}

async function handlePasswordRegister() {
  errorMsg.value = ''
  if (!form.value.phone) { errorMsg.value = '请输入手机号'; return }
  if (!/^1\d{10}$/.test(form.value.phone)) { errorMsg.value = '请输入正确的手机号'; return }
  if (!form.value.password) { errorMsg.value = '请设置密码'; return }
  if (form.value.password.length < 6) { errorMsg.value = '密码长度至少6位'; return }
  if (form.value.password !== confirmPassword.value) { errorMsg.value = '两次输入的密码不一致'; return }
  if (!agreedToTerms.value) { errorMsg.value = '请先阅读并同意用户协议'; return }
  try {
    await register(form.value.phone, form.value.password, form.value.nickname)
    router.replace({ path: '/login', query: { registered: form.value.phone } })
  } catch (err: any) {
    if (err?.response?.status === 409) {
      errorMsg.value = '该手机号已注册，请直接登录'
      alreadyRegistered.value = true
    } else {
      errorMsg.value = err?.response?.data?.detail || err?.message || '注册失败，请重试'
      alreadyRegistered.value = false
    }
  }
}

async function handleSmsRegister() {
  errorMsg.value = ''
  if (!form.value.phone) { errorMsg.value = '请输入手机号'; return }
  if (!form.value.smsCode) { errorMsg.value = '请输入验证码'; return }
  try { await loginBySms(form.value.phone, form.value.smsCode); router.replace({ path: '/login', query: { registered: form.value.phone } }) }
  catch (err: any) {
    if (err?.response?.status === 409) {
      errorMsg.value = '该手机号已注册，请直接登录'
      alreadyRegistered.value = true
    } else {
      errorMsg.value = err?.response?.data?.detail || '验证失败，请重试'
      alreadyRegistered.value = false
    }
  }
}

async function handleWechatRegister() {
  errorMsg.value = ''
  if (!form.value.wechatCode) { errorMsg.value = '请输入授权码'; return }
  try { await loginByWechat(form.value.wechatCode, form.value.nickname); router.replace({ path: '/login', query: { registered: '微信用户' } }) }
  catch (err: any) { errorMsg.value = err?.response?.data?.detail || '微信注册失败，请重试' }
}

function showTerms() {
  ElMessageBox.alert('欢迎使用旅游AI！使用本服务即表示您同意我们的服务条款和隐私政策。我们重视您的隐私并致力于保护您的个人信息。', '用户协议', { confirmButtonText: '我知道了', type: 'info' })
}
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

.auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 24px; background: $bg-warm; position: relative; overflow: hidden; font-family: 'Noto Sans SC', 'PingFang SC', sans-serif; }
.bg-layer { position: absolute; inset: 0; overflow: hidden; z-index: 0; }
.bg-orb { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.1; }
.bg-orb.orb-1 { width: 500px; height: 500px; background: rgba(184, 196, 184, 0.4); top: -150px; right: -100px; }
.bg-orb.orb-2 { width: 400px; height: 400px; background: rgba(232, 213, 208, 0.5); bottom: -100px; left: -80px; }

.auth-card { position: relative; z-index: 1; display: flex; max-width: 960px; width: 100%; min-height: 640px; background: $bg-white; border-radius: 24px; overflow: hidden; box-shadow: 0 8px 40px rgba(166, 139, 122, 0.12), 0 0 0 1px rgba(232, 213, 208, 0.3); }

.brand-panel { flex: 1; background: linear-gradient(160deg, $bg-oat 0%, #F0EBE3 100%); display: flex; align-items: center; padding: 48px 44px; position: relative; }
.brand-panel::after { content: ''; position: absolute; top: 0; right: 0; width: 1px; height: 100%; background: linear-gradient(180deg, transparent, rgba(166,139,122,0.15), transparent); }
.brand-content { position: relative; z-index: 1; width: 100%; }

.brand-logo { display: flex; align-items: center; gap: 14px; margin-bottom: 44px; cursor: pointer; }
.brand-icon { font-size: 36px; }
.brand-name { font-size: 22px; font-weight: 600; color: $text-primary; letter-spacing: 1px; display: block; }
.brand-en { font-size: 9px; color: $text-muted; letter-spacing: 2px; font-weight: 500; }

.brand-hero { margin-bottom: 36px; }
.brand-hero h2 { font-size: 28px; font-weight: 300; color: $text-primary; line-height: 1.4; margin-bottom: 14px; }
.brand-hero h2 .hero-accent { font-weight: 600; color: $brand-brown; }
.brand-hero p { font-size: 14px; color: $text-secondary; line-height: 1.7; }

.register-steps { display: flex; flex-direction: column; gap: 0; margin-bottom: 40px; }
.step-item { display: flex; align-items: center; gap: 14px; padding: 6px 0; }
.step-num { font-size: 11px; font-weight: 700; color: $text-secondary; letter-spacing: 1px; font-family: monospace; }
.step-info { display: flex; flex-direction: column; gap: 1px; }
.step-title { font-size: 14px; font-weight: 600; color: $text-primary; }
.step-desc { font-size: 12px; color: $text-secondary; }
.step-connector { width: 1px; height: 16px; background: $border; margin-left: 13px; }

.brand-quote { position: relative; }
.quote-mark { font-size: 40px; color: $brand-brown; line-height: 1; font-family: serif; display: block; margin-bottom: 4px; }
.brand-quote p { font-size: 13px; color: $text-secondary; line-height: 1.7; font-style: italic; margin-bottom: 14px; }
.quote-author { display: flex; align-items: center; gap: 12px; }
.author-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, $brand-nude, $brand-sage); display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600; color: white; }
.author-name { display: block; font-size: 13px; color: $text-primary; font-weight: 500; }
.author-role { display: block; font-size: 11px; color: $text-secondary; }

.form-panel { flex: 0.9; display: flex; align-items: center; justify-content: center; padding: 48px 44px; }
.form-container { width: 100%; max-width: 360px; }
.form-header { margin-bottom: 28px; }
.form-header h3 { font-size: 26px; font-weight: 600; color: $text-primary; margin-bottom: 6px; }
.form-header p { font-size: 14px; color: $text-muted; }

.auth-tabs { display: flex; position: relative; background: $bg-oat; border-radius: 12px; padding: 4px; margin-bottom: 24px; }
.tab-item { flex: 1; display: flex; align-items: center; justify-content: center; gap: 6px; padding: 10px 8px; border: none; background: transparent; border-radius: 10px; font-size: 13px; font-weight: 500; color: $text-muted; cursor: pointer; position: relative; z-index: 1; transition: color 0.3s; font-family: inherit; }
.tab-item:hover { color: $text-secondary; }
.tab-item.active { color: $brand-brown; }
.tab-indicator { position: absolute; top: 4px; left: 4px; width: calc((100% - 8px) / 3); height: calc(100% - 8px); background: $bg-white; border-radius: 10px; transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 1px 4px rgba(166,139,122,0.08); border: 1px solid $border; }

.alert { display: flex; align-items: flex-start; gap: 10px; padding: 12px 14px; border-radius: 10px; margin-bottom: 18px; font-size: 13px; line-height: 1.5; }
.alert-error { background: rgba(212,117,107,0.08); color: $danger; border: 1px solid rgba(212,117,107,0.2); }
.alert-success { background: rgba(143,175,138,0.08); color: $success; border: 1px solid rgba(143,175,138,0.2); }
.alert-icon { width: 18px; height: 18px; flex-shrink: 0; margin-top: 1px; }
.alert-title { font-weight: 600; margin-bottom: 2px; }
.alert-desc { opacity: 0.85; font-size: 12px; }
.alert-close { flex-shrink: 0; border: none; background: none; color: inherit; opacity: 0.5; cursor: pointer; font-size: 18px; padding: 0; line-height: 1; &:hover { opacity: 1; } }
.alert-link { display: inline-block; margin-top: 4px; font-size: 13px; font-weight: 600; color: inherit; text-decoration: underline; &:hover { opacity: 0.8; } }

.auth-form { display: flex; flex-direction: column; }
.input-group { margin-bottom: 16px; }
.input-label { display: block; font-size: 13px; font-weight: 500; color: $text-secondary; margin-bottom: 6px; }
.input-wrapper { display: flex; align-items: center; background: $bg-oat; border-radius: 10px; border: 1.5px solid transparent; transition: all 0.25s; overflow: hidden; }
.input-wrapper:focus-within { border-color: $brand-sage; box-shadow: 0 0 0 3px rgba(184,196,184,0.2); }
.input-prefix { padding-left: 14px; font-size: 16px; flex-shrink: 0; }
.input-suffix { padding-right: 14px; background: none; border: none; cursor: pointer; font-size: 16px; flex-shrink: 0; }
.input-field { flex: 1; padding: 13px 12px; background: transparent; border: none; outline: none; font-size: 15px; color: $text-primary; font-family: inherit; }
.input-field::placeholder { color: $text-muted; font-size: 14px; }

.password-strength { display: flex; align-items: center; gap: 12px; margin-top: -6px; margin-bottom: 18px; }
.strength-bars { display: flex; gap: 4px; flex: 1; }
.strength-bar { flex: 1; height: 4px; border-radius: 2px; background: $border; transition: background 0.3s; }
.strength-bar.active.weak { background: $danger; }
.strength-bar.active.medium { background: $brand-brown; }
.strength-bar.active.strong { background: $success; }
.strength-text { font-size: 12px; font-weight: 500; flex-shrink: 0; }
.strength-text.text-weak { color: $danger; }
.strength-text.text-medium { color: $brand-brown; }
.strength-text.text-strong { color: $success; }

.agreement-row { display: flex; align-items: center; gap: 2px; margin-bottom: 24px; }
.remember-me { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 13px; color: $text-secondary; }
.remember-me input[type="checkbox"] { display: none; }
.checkmark { width: 18px; height: 18px; border-radius: 5px; border: 1.5px solid $border; background: transparent; display: flex; align-items: center; justify-content: center; transition: all 0.2s; position: relative; }
.checkmark::after { content: ''; position: absolute; width: 5px; height: 9px; border: solid white; border-width: 0 2px 2px 0; transform: rotate(45deg) scale(0); transition: transform 0.15s; margin-top: -1px; }
.remember-me input:checked + .checkmark { background: $brand-sage; border-color: $brand-sage; }
.remember-me input:checked + .checkmark::after { transform: rotate(45deg) scale(1); }
.forgot-link { font-size: 13px; color: $brand-brown; cursor: pointer; }

.submit-btn { width: 100%; padding: 14px 0; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; letter-spacing: 2px; cursor: pointer; color: white; background: linear-gradient(135deg, $brand-nude 0%, $brand-sage 100%); box-shadow: 0 4px 16px rgba(184,196,184,0.3); transition: all 0.3s; font-family: inherit; }
.submit-btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 6px 24px rgba(184,196,184,0.4); }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.wechat-btn { background: linear-gradient(135deg, #7EC87E, #07C160) !important; }

.sms-row { display: flex; gap: 10px; }
.sms-input-wrap { flex: 1; }
.sms-btn { flex-shrink: 0; min-width: 110px; padding: 0 12px; border-radius: 10px; border: 1.5px solid $border; background: transparent; color: $brand-brown; font-size: 13px; font-weight: 500; cursor: pointer; font-family: inherit; transition: all 0.25s; }
.sms-btn:hover:not(:disabled) { border-color: $brand-brown; background: rgba(166,139,122,0.08); }
.sms-btn:disabled { color: $text-muted; border-color: $border; cursor: not-allowed; }
.sms-hint { text-align: center; margin-top: 14px; font-size: 12px; color: $text-muted; }

.wechat-qr { display: flex; justify-content: center; margin-bottom: 4px; }
.qr-placeholder { width: 140px; height: 140px; background: $bg-oat; border: 2px dashed $border; border-radius: 14px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; color: $text-muted; transition: all 0.3s; }
.qr-placeholder:hover { border-color: $brand-sage; color: $brand-sage; }
.qr-icon { font-size: 36px; }
.qr-placeholder p { font-size: 12px; }
.divider { display: flex; align-items: center; gap: 12px; margin: 18px 0; }
.divider-line { flex: 1; height: 1px; background: $border; }
.divider-text { font-size: 12px; color: $text-muted; white-space: nowrap; }

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
