import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

export function useAuth() {
  const store = useUserStore()
  const loading = ref(false)

  async function login(phone: string, password: string) {
    loading.value = true
    try {
      await store.login(phone, password)
    } finally {
      loading.value = false
    }
  }

  async function register(phone: string, password: string, smsCode: string, nickname: string) {
    loading.value = true
    try {
      return await store.register(phone, password, smsCode, nickname)
    } finally {
      loading.value = false
    }
  }

  async function sendSmsCode(phone: string) {
    return await store.sendSmsCode(phone)
  }

  async function verifySmsCode(phone: string, code: string) {
    return await store.verifySmsCode(phone, code)
  }

  async function loginBySms(phone: string, code: string) {
    loading.value = true
    try {
      await store.loginBySms(phone, code)
    } finally {
      loading.value = false
    }
  }

  async function loginByWechat(code: string, nickname?: string, avatarUrl?: string) {
    loading.value = true
    try {
      await store.loginByWechat(code, nickname, avatarUrl)
    } finally {
      loading.value = false
    }
  }

  function logout() {
    store.logout()
  }

  return {
    ...store,
    loading,
    login,
    register,
    sendSmsCode,
    verifySmsCode,
    loginBySms,
    loginByWechat,
    logout,
  }
}
