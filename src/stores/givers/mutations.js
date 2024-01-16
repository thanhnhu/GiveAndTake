import * as types from './mutation-types'

export default {
  [types.FETCH_GIVERS_REQUEST](state) {
    state.fetchingData = true
    state.error = null
    state.givers = []
  },
  [types.FETCH_GIVERS_SUCCESS](state, result) {
    state.fetchingData = false
    state.error = null
    state.total = result.count
    state.givers = [...result.results]
  },
  [types.FETCH_GIVERS_FAILURE](state, { error }) {
    state.fetchingData = false
    state.error = error
    state.givers = []
  },

  [types.ADD_GIVER_REQUEST](state) {
    state.fetchingData = true
    state.error = null
  },
  [types.ADD_GIVER_SUCCESS](state, { giver }) {
    state.fetchingData = false
    state.error = null
    state.givers = [giver, ...state.givers]
  },
  [types.ADD_GIVER_FAILURE](state, { error }) {
    state.fetchingData = false
    state.error = error
  },

  [types.SET_ACTIVE_GIVER](state, giverId) {
    state.fetchingData = false
    state.error = null
    let index = state.givers.findIndex(r => r.id === giverId)
    state.givers[index].active = !state.givers[index].active;
  },

  [types.REMOVE_GIVER_SUCCESS](state, giverId) {
    state.fetchingData = false
    state.error = null
    let index = state.givers.findIndex(r => r.id === giverId)
    state.givers.splice(index, 1);
  },
  [types.REMOVE_GIVER_FAILURE](state, { error }) {
    state.fetchingData = false
    state.error = error
  },
}
