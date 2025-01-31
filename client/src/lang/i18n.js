import { createI18n } from 'vue-i18n'
import vnMessage from './vi.json'
import enMessage from './en.json'

const messages = {
  vi: vnMessage,
  en: enMessage,
}

const createI18nInstance = () => {
  return createI18n({
    legacy: false,
    globalInjection: true,
    locale: 'vi',
    fallbackLocale: 'vi',
    messages,
  })
}

export const i18n = createI18nInstance()