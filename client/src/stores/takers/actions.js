import * as types from './mutation-types'
import takerService from '../../services/takerService'

export default {
  getTakers({ commit }, filter) {
    commit(types.FETCH_TAKERS_REQUEST)

    takerService.fetchTakers(filter)
      .then(takers => commit(types.FETCH_TAKERS_SUCCESS, takers))
      .catch(error => commit(types.FETCH_TAKERS_FAILURE, { error }))
  },
  addTaker({ commit }, taker) {
    commit(types.ADD_TAKER_REQUEST)
    takerService.postTaker(taker)
      .then(taker => commit(types.ADD_TAKER_SUCCESS, { taker }))
      .catch(error => commit(types.ADD_TAKER_FAILURE, { error }))
  },
  stopDonate({ commit }, takerId) {
    takerService.stopDonate(takerId)
      .then(() => commit(types.STOP_DONATE_TAKER, takerId))
  },
  removeTaker({ commit }, takerId) {
    takerService.removeTaker(takerId)
      .then(() => commit(types.REMOVE_TAKER_SUCCESS, takerId))
      .catch(error => commit(types.REMOVE_TAKER_FAILURE, { error }))
  },

  addDonate({ commit }, donate) {
    commit(types.DONATE_TAKER_REQUEST)
    takerService.addDonate(donate)
      .then(donate => commit(types.DONATE_TAKER_SUCCESS, donate))
      .catch(error => commit(types.DONATE_TAKER_FAILURE, { error }))
  },
  updateDonate({ commit }, donate) {
    commit(types.UPDATE_DONATE_REQUEST)
    takerService.updateDonate(donate)
      .then(donate => commit(types.UPDATE_DONATE_SUCCESS, donate))
      .catch(error => commit(types.UPDATE_DONATE_FAILURE, { error }))
  },
  removeDonate({ commit }, donateId) {
    takerService.removeDonate(donateId)
      .then(response => commit(types.REMOVE_DONATE_SUCCESS, response.data))
      .catch(error => commit(types.REMOVE_DONATE_FAILURE, { error }))
  },
}
