import api from '@/services/api'

const fetchCities = async () => {
  try {
    const response = await api.get('cities/')
    return response
  } catch (error) {
    console.error('Error fetching cities:', error)
    throw error
  }
}

export const cityService = {
  fetchCities
};