import { defineStore } from 'pinia'
import { i18n } from '@/lang/i18n'
import cityService from '@/services/cityService'

export const citiesStoreObj = defineStore('cities', {
  state: () => ({
    fetchingData: true,
    error: null,
    cities: [],
    total: 0
  }),

  getters: {
    optionCities: (state) => {
      return [{ id: null, name: i18n.global.t('common.select_city') }, ...state.cities]
    }
  },

  actions: {
    async getCities() {
      this.fetchingData = true
      this.error = null
      this.cities = []

      try {
        const citiesData = await cityService.fetchCities()

        const first = [15, 58]
        const sortedCities = citiesData.sort((x, y) => {
          const xi = first.indexOf(x.id)
          const yi = first.indexOf(y.id)
          if (xi !== -1 && yi !== -1) return xi - yi
          if (xi !== -1) return -1
          if (yi !== -1) return 1
          return 0
        })

        this.cities = sortedCities
        this.total = sortedCities.length
        this.fetchingData = false
        this.error = null
      } catch (err) {
        this.fetchingData = false
        this.error = err
        this.cities = []
      }
    }
  }
})