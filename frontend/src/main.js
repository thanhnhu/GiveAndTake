import { createApp, markRaw } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from '@/App.vue'
import router from '@/router'
import { i18n } from "@/lang/i18n"
import installBootstrap from '@/bootstrap';
import '@/validation'

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)
pinia.use(({ store }) => {
  store.router = markRaw(router)
})

app.use(pinia)
app.use(router)
app.use(i18n)

installBootstrap(app);

app.mount('#app')

app.config.errorHandler = (error, vm, info) => {
  console.log('Exception: ', error)
  if (error?.statusCode === 401) {
    window.location = '/'
  }
}

window.onerror = function (message, source, lineno, colno, error) {
  console.log('Exception: ', error)
}

export { app }