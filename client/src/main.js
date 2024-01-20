import Vue from 'vue'
import App from '@/App.vue'
import '@/bootstrap'
import '@/validation'
import '@/utils'

import router from '@/router'
import store from '@/stores'
import i18n from '@/lang/i18n'


Vue.config.productionTip = false

export const vue = new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
})

vue.$mount('#app')
