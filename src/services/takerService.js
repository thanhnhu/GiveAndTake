import api from '@/services/api'
import { headers } from './headers'

export default {
  fetchTakers(filter) {
    let params = { params: filter }
    let config = { ...headers(), ...params }
    return api.get(`takers/`, config)
      .then(response => response.data)
  },
  postTaker(newTaker) {
    return api.post(`takers/`, newTaker, headers())
      .then(response => response.data)
  },
  stopDonate(takerId) {
    return api.patch(`takers/${takerId}/stop_donate/`, null, headers())
      .then(response => response.data)
  },
  removeTaker(takerId) {
    return api.delete(`takers/${takerId}`, headers())
      .then(response => response.data)
  },

  addDonate(donate) {
    return api.post(`donates/`, donate, headers())
      .then(response => response.data)
  },
  updateDonate(donate) {
    return api.patch(`donates/${donate.id}/`, donate, headers())
      .then(response => response.data)
  },
  removeDonate(donateId) {
    return api.delete(`donates/${donateId}`, headers())
      .then(response => response.data)
  },
}