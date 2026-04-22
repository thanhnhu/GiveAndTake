import { setActivePinia, createPinia } from 'pinia'
import { citiesStoreObj } from '@/stores/cities'
import cityService from '@/services/cityService'
import { flushPromises } from '@vue/test-utils'

jest.mock('@/services/cityService')
jest.mock('@/lang/i18n', () => ({
  i18n: {
    global: {
      t: (key) => key,
    },
  },
}))

const mockCities = [
  { id: 15, name: 'Đà Nẵng' },
  { id: 58, name: 'TP. Hồ Chí Minh' },
  { id: 1, name: 'An Giang' },
  { id: 2, name: 'Bà Rịa - Vũng Tàu' },
]

describe('Cities Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    jest.clearAllMocks()
  })

  // ─── getCities ───────────────────────────────────────────────────────────

  it('getCities: populates cities and total on success', async () => {
    const store = citiesStoreObj()
    cityService.fetchCities.mockResolvedValue([...mockCities])

    await store.getCities()
    await flushPromises()

    expect(store.cities).toHaveLength(4)
    expect(store.total).toBe(4)
    expect(store.fetchingData).toBe(false)
    expect(store.error).toBeNull()
  })

  it('getCities: sorts priority cities (id 15 and 58) first', async () => {
    const store = citiesStoreObj()
    cityService.fetchCities.mockResolvedValue([...mockCities])

    await store.getCities()
    await flushPromises()

    expect(store.cities[0].id).toBe(15)
    expect(store.cities[1].id).toBe(58)
  })

  it('getCities: sets error and clears cities on failure', async () => {
    const store = citiesStoreObj()
    const err = new Error('Fetch failed')
    cityService.fetchCities.mockRejectedValue(err)

    await store.getCities()
    await flushPromises()

    expect(store.cities).toEqual([])
    expect(store.error).toBe(err)
    expect(store.fetchingData).toBe(false)
  })

  // ─── optionCities getter ─────────────────────────────────────────────────

  it('optionCities: prepends null-id placeholder option', async () => {
    const store = citiesStoreObj()
    cityService.fetchCities.mockResolvedValue([mockCities[0]])

    await store.getCities()
    await flushPromises()

    expect(store.optionCities[0].id).toBeNull()
    expect(store.optionCities).toHaveLength(2)
  })

  it('optionCities: returns only placeholder when cities is empty', () => {
    const store = citiesStoreObj()

    expect(store.optionCities).toHaveLength(1)
    expect(store.optionCities[0].id).toBeNull()
  })
})
