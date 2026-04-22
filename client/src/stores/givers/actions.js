import * as types from './mutation-types'
import giverService from '../../services/giverService'

export default {
  getGivers({ commit }, filter) {
    commit(types.FETCH_GIVERS_REQUEST)

    giverService.fetchGivers(filter)
      .then(givers => commit(types.FETCH_GIVERS_SUCCESS, givers))
      .catch(error => commit(types.FETCH_GIVERS_FAILURE, { error }))
  },
  addGiver({ commit }, giver) {
    commit(types.ADD_GIVER_REQUEST)
    giverService.postGiver(giver)
      .then(giver => commit(types.ADD_GIVER_SUCCESS, { giver }))
      .catch(error => commit(types.ADD_GIVER_FAILURE, { error }))
  },
  setActive({ commit }, giverId) {
    giverService.setActive(giverId)
      .then(() => commit(types.SET_ACTIVE_GIVER, giverId))
  },
  removeGiver({ commit }, giverId) {
    giverService.removeGiver(giverId)
      .then(() => commit(types.REMOVE_GIVER_SUCCESS, giverId))
      .catch(error => commit(types.REMOVE_GIVER_FAILURE, { error }))
  },
}
