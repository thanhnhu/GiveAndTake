import { defineStore } from 'pinia'
import { arrayOrderedToObject } from '@/helpers'
import takerService from '@/services/takerService'

export const takersStoreObj = defineStore('takers', {
  state: () => ({
    fetchingData: true,
    error: null,
    total: 0,
    takers: []
  }),

  getters: {
    takersMap: (state) => {
      return { ...arrayOrderedToObject(state.takers, "id") }
    }
  },

  actions: {
    async getTakers(filter) {
      this.fetchingData = true
      this.error = null
      this.takers = []

      try {
        const result = await takerService.fetchTakers(filter)
        this.takers = result.results
        this.total = result.count
        this.fetchingData = false
      } catch (error) {
        this.fetchingData = false
        this.error = error
        this.takers = []
      }
    },

    async addTaker(taker) {
      this.fetchingData = true
      this.error = null

      try {
        const newTaker = await takerService.postTaker(taker)
        this.fetchingData = false
        this.takers = [newTaker, ...this.takers]
      } catch (error) {
        this.fetchingData = false
        this.error = error
      }
    },

    async stopDonate(takerId) {
      try {
        await takerService.stopDonate(takerId)
        const index = this.takers.findIndex(r => r.id === takerId)
        this.takers[index].stop_donate = !this.takers[index].stop_donate
      } catch (error) {
        this.error = error
      }
    },

    async removeTaker(takerId) {
      try {
        await takerService.removeTaker(takerId)
        this.takers = this.takers.filter(r => r.id !== takerId)
      } catch (error) {
        this.error = error
      }
    },

    async addDonate(donate) {
      try {
        await takerService.addDonate(donate)
        const index = this.takers.findIndex(r => r.id === donate.taker)
        this.takers[index].donates.push(donate)
      } catch (error) {
        this.error = error
      }
    },

    async updateDonate(donate) {
      try {
        await takerService.updateDonate(donate)
        const takerIndex = this.takers.findIndex(r => r.id === donate.taker)
        const donateIndex = this.takers[takerIndex].donates.findIndex(d => d.id === donate.id)
        this.takers[takerIndex].donates[donateIndex] = donate
      } catch (error) {
        this.error = error
      }
    },

    async removeDonate(donateId) {
      try {
        await takerService.removeDonate(donateId)
        const takerIndex = this.takers.findIndex(r => r.donates.some(d => d.id === donateId))
        this.takers[takerIndex].donates = this.takers[takerIndex].donates.filter(d => d.id !== donateId)
      } catch (error) {
        this.error = error
      }
    }
  }
}) 