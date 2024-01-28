import Vue from 'vue'
import VueI18n from 'vue-i18n'
import vnMessage from './vi.json'
import enMessage from './en.json'


Vue.use(VueI18n)

const messages = {
  vi: vnMessage,
  en: enMessage,
}

const i18n = new VueI18n({
  locale: 'en', // set locale
  messages,
  fallbackLocale: 'en',
})
export default i18n