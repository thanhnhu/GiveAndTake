import { defineStore } from 'pinia'
import { i18n } from "@/lang/i18n"

export const langStoreObj = defineStore('langs', {
  state: () => ({
    locale: i18n.global.locale
  }),

  getters: {
    getLang: (state) => state.locale
  },

  actions: {
    setLang(newLocale) {
      i18n.global.locale = newLocale
      this.locale = newLocale
    }
  },

  persist: true
})
