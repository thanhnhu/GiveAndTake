import { defineStore } from 'pinia'
import giverService from '@/services/giverService'

export const giversStoreObj = defineStore('givers', {
  state: () => ({
    fetchingData: true,
    error: null,
    total: 0,
    givers: []
  }),

  getters: {
    giversMap: (state) => {
      return state.givers.reduce((acc, giver) => {
        acc[giver.id] = giver
        return acc
      }, {})
    }
  },

  actions: {
    async getGivers(filter) {
      try {
        this.fetchingData = true
        const response = await giverService.fetchGivers(filter)
        this.givers = response.results
        this.total = response.count
        this.fetchingData = false
        this.error = null
      } catch (error) {
        this.fetchingData = false
        this.error = error
        this.givers = []
        this.total = 0
      }
    },

    async addGiver(newGiver) {
      try {
        const giver = await giverService.postGiver(newGiver)
        this.givers.unshift(giver)
      } catch (error) {
        this.error = error
      }
    },

    async setActive(giverId) {
      try {
        await giverService.setActive(giverId)
        const giver = this.givers.find(r => r.id === giverId)
        if (giver) {
          giver.active = !giver.active
        }
      } catch (error) {
        this.error = error
      }
    },

    async removeGiver(giverId) {
      try {
        await giverService.removeGiver(giverId)
        const index = this.givers.findIndex(r => r.id === giverId)
        if (index !== -1) {
          this.givers.splice(index, 1)
        }
      } catch (error) {
        this.error = error
      }
    }
  }
}) 