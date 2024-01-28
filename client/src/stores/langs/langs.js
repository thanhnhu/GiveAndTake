import { vue } from '@/main'

const getters = {
  getLang: () => vue.$i18n.locale
}

const mutations = {
  SET_LANG(state, payload) {
    vue.$i18n.locale = payload
  }
}

const actions = {
  setLang({ commit }, payload) {
    commit('SET_LANG', payload)
  }
}

export default {
  namespaced: true,
  getters,
  mutations,
  actions
}
