import * as types from './mutation-types'

export default {
  [types.FETCH_TAKERS_REQUEST](state) {
    state.fetchingData = true
    state.error = null
    state.takers = []
  },
  [types.FETCH_TAKERS_SUCCESS](state, result) {
    state.fetchingData = false
    state.error = null
    state.total = result.count
    state.takers = [...result.results]
  },
  [types.FETCH_TAKERS_FAILURE](state, { error }) {
    state.fetchingData = false
    state.error = error
    state.takers = []
  },

  [types.ADD_TAKER_REQUEST](state) {
    state.fetchingData = true
    state.error = null
  },
  [types.ADD_TAKER_SUCCESS](state, { taker }) {
    state.fetchingData = false
    state.error = null
    state.takers = [taker, ...state.takers]
  },
  [types.ADD_TAKER_FAILURE](state, { error }) {
    state.fetchingData = false
    state.error = error
  },

  [types.STOP_DONATE_TAKER](state, takerId) {
    state.fetchingData = false
    state.error = null
    let index = state.takers.findIndex(r => r.id === takerId)
    state.takers[index].stop_donate = !state.takers[index].stop_donate;
  },

  [types.REMOVE_TAKER_SUCCESS](state, takerId) {
    state.fetchingData = false
    state.error = null
    let index = state.takers.findIndex(r => r.id === takerId)
    state.takers.splice(index, 1);
  },
  [types.REMOVE_TAKER_FAILURE](state, { error }) {
    state.fetchingData = false
    state.error = error
  },

  [types.DONATE_TAKER_REQUEST](state) {
    state.fetchingData = true
    state.error = null
  },
  [types.DONATE_TAKER_SUCCESS](state, donate) {
    state.fetchingData = false
    state.error = null
    let index = state.takers.findIndex(r => r.id === donate.taker)
    state.takers[index].donates.push(donate);
  },
  [types.DONATE_TAKER_FAILURE](state, { error }) {
    state.fetchingData = false
    state.error = error
  },

  [types.UPDATE_DONATE_REQUEST](state) {
    state.fetchingData = true
    state.error = null
  },
  [types.UPDATE_DONATE_SUCCESS](state, donate) {
    state.fetchingData = false
    state.error = null
    let takerIdx = state.takers.findIndex(r => r.id === donate.taker)
    let donateIdx = state.takers[takerIdx].donates.findIndex(r => r.id === donate.id)
    state.takers[takerIdx].donates[donateIdx] = donate;
  },
  [types.UPDATE_DONATE_FAILURE](state, { error }) {
    state.fetchingData = false
    state.error = error
  },

  [types.REMOVE_DONATE_SUCCESS](state, deleted) {
    state.fetchingData = false
    state.error = null
    
    let takerIdx = state.takers.findIndex(r => r.id === deleted.taker)
    let donateIdx = state.takers[takerIdx].donates.findIndex(r => r.id === deleted.id)
    state.takers[takerIdx].donates.splice(donateIdx, 1);
  },
  [types.REMOVE_DONATE_FAILURE](state, { error }) {
    state.fetchingData = false
    state.error = error
  },
}
