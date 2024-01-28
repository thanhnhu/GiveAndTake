import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import createLogger from 'vuex/dist/logger'

import langs from './langs/langs'
import users from './users/'
import messages from './messages/messages'
import cities from './cities/cities'
import takers from './takers/'
import givers from './givers/'
import uploads from './uploads/'


Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'

const plugins = [createPersistedState()]
if (debug) plugins.push(createLogger())

export default new Vuex.Store({
  strict: debug,
  plugins: plugins,
  modules: {
    langs,
    uploads,
    users,
    messages,
    cities,
    takers,
    givers
  }
})