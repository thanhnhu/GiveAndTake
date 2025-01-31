import { defineStore } from 'pinia'
import { messageService } from '@/services/messageService'

export const messagesStoreObj = defineStore('messages', {
  state: () => ({
    messages: [],
    fetchingData: false,
    error: null
  }),

  actions: {
    async getMessages() {
      try {
        this.fetchingData = true
        const messageService = messageService()
        const messages = await messageService.fetchMessages()
        this.messages = messages
        this.fetchingData = false
        this.error = null
      } catch (error) {
        this.fetchingData = false
        this.error = error
        this.messages = []
      }
    },

    async addMessage(message) {
      try {
        const messageService = messageService()
        const newMessage = await messageService.postMessage(message)
        this.messages.unshift(newMessage)
        this.error = null
      } catch (error) {
        this.error = error
      }
    },

    async deleteMessage(messageId) {
      try {
        const messageService = messageService()
        await messageService.deleteMessage(messageId)
        const index = this.messages.findIndex(msg => msg.pk === messageId)
        if (index !== -1) {
          this.messages.splice(index, 1)
        }
        this.error = null
      } catch (error) {
        this.error = error
      }
    }
  }
})