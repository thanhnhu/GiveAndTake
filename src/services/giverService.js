import api from '@/services/api'
import { headers } from './headers'

export default {
  fetchGivers(filter) {
    let params = { params: filter }
    let config = { ...headers(), ...params }
    return api.get(`givers/`, config)
      .then(response => response.data)
  },
  postGiver(newGiver) {
    return api.post(`givers/`, newGiver, headers())
      .then(response => response.data)
  },
  setActive(giverId) {
    return api.patch(`givers/${giverId}/set_active/`, null, headers())
      .then(response => response.data)
  },
  removeGiver(giverId) {
    return api.delete(`givers/${giverId}`, headers())
      .then(response => response.data)
  },
}