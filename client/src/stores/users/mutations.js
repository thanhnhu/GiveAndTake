import * as types from './mutation-types'

export default {
  [types.LOGIN_REQUEST](state) {
    state.fetchingData = true
    state.error = null
  },
  [types.LOGIN_SUCCESS](state, data) {
    state.fetchingData = false
    state.error = null
    state.token = data.token
    state.user = JSON.parse(data.user)
  },
  [types.LOGIN_FAILURE](state, { error }) {
    state.fetchingData = false
    state.error = error
    state.user = null
  },
  [types.LOGOUT](state) {
    state.token = null
    state.user = null
  },
  [types.REGISTER_REQUEST](state) {
    state.fetchingData = true
    state.error = null
  },
  [types.REGISTER_SUCCESS](state) {
    state.fetchingData = false
    state.error = null
  },
  [types.REGISTER_FAILURE](state, error) {
    state.fetchingData = false
    state.error = error
  },
}
