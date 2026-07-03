import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UserInfo } from '@/types/common'
import { userAPI } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const user = ref<UserInfo | null>(null)
  const isLoggedIn = ref(!!localStorage.getItem('access_token'))

  // Init auth state from localStorage
  async function initAuth() {
    const token = localStorage.getItem('access_token')
    if (token) {
      try {
        await fetchUser()
      } catch {
        logout()
      }
    }
  }

  // Password login
  async function login(phone: string, password: string) {
    const { data } = await userAPI.login(phone, password)
    _saveTokens(data.data)
    await fetchUser()
  }

  // Password register — phone + password only, no SMS needed
  async function register(phone: string, password: string, nickname: string) {
    const { data } = await userAPI.register(phone, password, nickname)
    return data.data
  }

  // SMS: send code
  async function sendSmsCode(phone: string) {
    const { data } = await userAPI.sendSmsCode(phone)
    return data.data
  }

  // SMS: verify code (check code validity without login)
  async function verifySmsCode(phone: string, code: string) {
    const { data } = await userAPI.verifySmsCode(phone, code)
    return data.data
  }

  // SMS: login with code
  async function loginBySms(phone: string, code: string) {
    const { data } = await userAPI.loginBySms(phone, code)
    _saveTokens(data.data)
    await fetchUser()
  }

  // WeChat login
  async function loginByWechat(code: string, nickname?: string, avatarUrl?: string) {
    const { data } = await userAPI.loginByWechat(code, nickname, avatarUrl)
    _saveTokens(data.data)
    await fetchUser()
  }

  async function fetchUser() {
    try {
      const { data } = await userAPI.getMe()
      user.value = data.data
    } catch {
      logout()
    }
  }

  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    user.value = null
    isLoggedIn.value = false
  }

  function _saveTokens(tokens: { access_token: string; refresh_token: string }) {
    localStorage.setItem('access_token', tokens.access_token)
    localStorage.setItem('refresh_token', tokens.refresh_token)
    isLoggedIn.value = true
  }

  return {
    user,
    isLoggedIn,
    initAuth,
    login,
    register,
    sendSmsCode,
    verifySmsCode,
    loginBySms,
    loginByWechat,
    fetchUser,
    logout,
  }
})
