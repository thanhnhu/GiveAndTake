import api from '@/services/api'
import { headers } from '@/services/headers'

export default {
  async fetchMessages() {
    try {
      return await api.get('messages/', headers())
    } catch (error) {
      console.error('Error fetching messages:', error)
      throw error
    }
  },

  async postMessage(payload) {
    try {
      return await api.post('messages/', payload, headers())
    } catch (error) {
      console.error('Error posting message:', error)
      throw error
    }
  },

  async deleteMessage(msgId) {
    try {
      return await api.delete(`messages/${msgId}`, headers())
    } catch (error) {
      console.error('Error deleting message:', error)
      throw error
    }
  }
}