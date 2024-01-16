import api from '@/services/api'

export default {
  fetchCities() {
    return api.get(`cities/`)
      .then(response => response.data)
  }
}