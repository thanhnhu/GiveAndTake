import api from '@/services/api'
import { headers } from '@/services/headers'

export const messageService = () => {
  const fetchMessages = async () => {
    try {
      const response = await api.get('messages/', headers())
      return response.data
    } catch (error) {
      console.error('Error fetching messages:', error)
      throw error
    }
  }

  const postMessage = async (payload) => {
    try {
      const response = await api.post('messages/', payload, headers())
      return response.data
    } catch (error) {
      console.error('Error posting message:', error)
      throw error
    }
  }

  const deleteMessage = async (msgId) => {
    try {
      const response = await api.delete(`messages/${msgId}`, headers())
      return response.data
    } catch (error) {
      console.error('Error deleting message:', error)
      throw error
    }
  }

  return {
    fetchMessages,
    postMessage,
    deleteMessage
  }
}