import api from '@/services/api'
import { headers } from '@/services/headers'

const userService = {
  async login(username, password) {
    try {
      return await api.post('auth/', { username, password })
    } catch (error) {
      console.error('Error logging in:', error)
      throw error
    }
  },

  async register(user) {
    try {
      return await api.post('users/', user)
    } catch (error) {
      console.error('Error registering user:', error)
      throw error
    }
  },

  async getUser(userId) {
    try {
      return await api.get(`users/${userId}`, headers())
    } catch (error) {
      console.error('Error getting user:', error)
      throw error
    }
  },

  async updateUser(user) {
    try {
      return await api.put(`users/${user.id}`, user, headers())
    } catch (error) {
      console.error('Error updating user:', error)
      throw error
    }
  },

  async deleteUser(userId) {
    try {
      return await api.delete(`users/${userId}`, headers())
    } catch (error) {
      console.error('Error deleting user:', error)
      throw error
    }
  }
}

export default userService