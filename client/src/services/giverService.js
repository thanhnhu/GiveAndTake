import api from '@/services/api'
import { headers } from '@/services/headers'

const giverService = {
  async fetchGivers(filter) {
    try {
      const params = { params: filter }
      const config = { ...headers(), ...params }
      return await api.get('givers/', config)
    } catch (error) {
      console.error('Error fetching givers:', error)
      throw error
    }
  },

  async postGiver(newGiver) {
    try {
      const response = await api.post('givers/', newGiver, headers())
      return response.data
    } catch (error) {
      console.error('Error creating giver:', error)
      throw error
    }
  },

  async setActive(giverId) {
    try {
      const response = await api.patch(`givers/${giverId}/set_active/`, null, headers())
      return response.data
    } catch (error) {
      console.error('Error setting giver active:', error)
      throw error
    }
  },

  async removeGiver(giverId) {
    try {
      const response = await api.delete(`givers/${giverId}`, headers())
      return response.data
    } catch (error) {
      console.error('Error removing giver:', error)
      throw error
    }
  }
}

export default giverService