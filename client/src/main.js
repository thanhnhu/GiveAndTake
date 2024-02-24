import Vue from 'vue'
import App from '@/App.vue'
import '@/bootstrap'
import '@/validation'
import '@/utils'

import router from '@/router'
import store from '@/stores'
import i18n from '@/lang/i18n'

Vue.config.productionTip = false

// eslint-disable-next-line
Vue.config.errorHandler = (error, vm, info) => {
  console.log('Exception: ', error)
  if (error && error.statusCode === 401) {
    window.location = '/'
  }
}

// eslint-disable-next-line
window.onerror = function (message, source, lineno, colno, error) {
  console.log('Exception: ', error)
}

export const vue = new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
})

vue.$mount('#app')