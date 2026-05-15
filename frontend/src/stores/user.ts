import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UserProfile } from '@/api/types/user'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const profile = ref<UserProfile | null>(null)

  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setProfile = (userProfile: UserProfile) => {
    profile.value = userProfile
  }

  const clearAuth = () => {
    token.value = ''
    profile.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    profile,
    setToken,
    setProfile,
    clearAuth,
    nickname: profile.value?.nickname,
    avatar: profile.value?.avatar_url,
    membership_type: profile.value?.membership_type
  }
})