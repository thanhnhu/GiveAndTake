import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useI18n } from 'vue-i18n'
import { cityService } from '@/services/cityService'

export const citiesStoreObj = defineStore('cities', () => {
  // state
  const fetchingData = ref(true)
  const error = ref(null)
  const cities = ref([])

  // getters
  const optionCities = computed(() => {
    const { t } = useI18n()
    return [{ id: null, name: t('common.select_city') }, ...cities.value]
  })

  // actions
  async function getCities() {
    fetchingData.value = true
    error.value = null
    cities.value = []
    
    try {
      const citiesData = await cityService.fetchCities()
      
      const first = [15, 58]
      const sortedCities = citiesData.sort((x, y) => 
        first.includes(x.id) ? -1 : first.includes(y.id) ? 1 : 0
      )
      
      cities.value = sortedCities
      fetchingData.value = false
      error.value = null
    } catch (err) {
      fetchingData.value = false
      error.value = err
      cities.value = []
    }
  }

  return {
    fetchingData,
    error,
    cities,
    optionCities,
    getCities
  }
})