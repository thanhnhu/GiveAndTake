import { defineStore } from 'pinia'
import { toastMessage } from '@/helpers'
import { i18n } from "@/lang/i18n"
import userService from '@/services/userService'

export const userStoreObj = defineStore('users', {
  state: () => ({
    token: null,
    user: null,
    fetchingData: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token
  },

  actions: {
    async login({ username, password }) {
      this.fetchingData = true
      this.error = null

      try {
        const response = await userService.login(username, password)
        this.token = response.token
        this.user = JSON.parse(response.user)
        this.fetchingData = false
        this.router.push('/');
        toastMessage(i18n.global.t('user.messages.login_success'))
      } catch (error) {
        this.fetchingData = false
        this.error = error
        this.user = null
      }
    },

    logout() {
      this.token = null
      this.user = null
      this.router.push("/")
      // Note: You'll need to update this to use the takers store with Pinia
      // const takersStore = takersStoreObj()
      // takersStore.getTakers()
    },

    async register(user) {
      this.fetchingData = true
      this.error = null

      try {
        await userService.register(user)
        this.fetchingData = false
        this.router.push('/login')
        toastMessage(i18n.global.t('user.messages.register_success'))
      } catch (error) {
        this.fetchingData = false
        this.error = error
      }
    }
  },

  persist: true
}) 