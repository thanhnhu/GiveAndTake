import { setActivePinia, createPinia } from 'pinia'
import { giversStoreObj } from '@/stores/givers'
import giverService from '@/services/giverService'
import { flushPromises } from '@vue/test-utils'

jest.mock('@/services/giverService')

const mockGiver = {
  id: 'giver-uuid-1',
  number: 1,
  name: 'Test Giver',
  phone: '0900000001',
  address: 'Hà Nội',
  city: 1,
  description: '',
  images: [],
  active: true,
  can_edit: true,
  can_delete: false,
}

describe('Givers Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    jest.clearAllMocks()
  })

  // ─── getGivers ───────────────────────────────────────────────────────────

  it('getGivers: populates givers and total on success', async () => {
    const store = giversStoreObj()
    giverService.fetchGivers.mockResolvedValue({ results: [mockGiver], count: 1 })

    await store.getGivers()
    await flushPromises()

    expect(store.givers).toEqual([mockGiver])
    expect(store.total).toBe(1)
    expect(store.fetchingData).toBe(false)
    expect(store.error).toBeNull()
  })

  it('getGivers: sets error and clears givers on failure', async () => {
    const store = giversStoreObj()
    const err = new Error('Network error')
    giverService.fetchGivers.mockRejectedValue(err)

    await store.getGivers()
    await flushPromises()

    expect(store.givers).toEqual([])
    expect(store.total).toBe(0)
    expect(store.error).toBe(err)
    expect(store.fetchingData).toBe(false)
  })

  // ─── addGiver ────────────────────────────────────────────────────────────

  it('addGiver: prepends server response to givers array', async () => {
    const store = giversStoreObj()
    store.givers = [{ ...mockGiver, id: 'giver-uuid-0' }]
    const newGiver = { ...mockGiver, id: 'giver-uuid-new', number: 2 }
    giverService.postGiver.mockResolvedValue(newGiver)

    await store.addGiver({ name: 'New', phone: '09', city: 1, address: 'HN' })
    await flushPromises()

    expect(store.givers[0]).toEqual(newGiver)
    expect(store.givers).toHaveLength(2)
  })

  it('addGiver: sets error on failure', async () => {
    const store = giversStoreObj()
    const err = new Error('Server error')
    giverService.postGiver.mockRejectedValue(err)

    await store.addGiver({ name: 'X' })
    await flushPromises()

    expect(store.error).toBe(err)
  })

  // ─── setActive ───────────────────────────────────────────────────────────

  it('setActive: toggles active flag from true to false', async () => {
    const store = giversStoreObj()
    store.givers = [{ ...mockGiver, active: true }]
    giverService.setActive.mockResolvedValue({})

    await store.setActive('giver-uuid-1')
    await flushPromises()

    expect(store.givers[0].active).toBe(false)
  })

  it('setActive: toggles active flag from false to true', async () => {
    const store = giversStoreObj()
    store.givers = [{ ...mockGiver, active: false }]
    giverService.setActive.mockResolvedValue({})

    await store.setActive('giver-uuid-1')
    await flushPromises()

    expect(store.givers[0].active).toBe(true)
  })

  it('setActive: sets error on failure', async () => {
    const store = giversStoreObj()
    store.givers = [{ ...mockGiver }]
    const err = new Error('Toggle failed')
    giverService.setActive.mockRejectedValue(err)

    await store.setActive('giver-uuid-1')
    await flushPromises()

    expect(store.error).toBe(err)
    expect(store.givers[0].active).toBe(true)
  })

  // ─── removeGiver ─────────────────────────────────────────────────────────

  it('removeGiver: removes giver from array', async () => {
    const store = giversStoreObj()
    store.givers = [{ ...mockGiver }]
    giverService.removeGiver.mockResolvedValue({})

    await store.removeGiver('giver-uuid-1')
    await flushPromises()

    expect(store.givers).toHaveLength(0)
  })

  it('removeGiver: sets error on failure', async () => {
    const store = giversStoreObj()
    store.givers = [{ ...mockGiver }]
    const err = new Error('Delete failed')
    giverService.removeGiver.mockRejectedValue(err)

    await store.removeGiver('giver-uuid-1')
    await flushPromises()

    expect(store.error).toBe(err)
    expect(store.givers).toHaveLength(1)
  })

  // ─── giversMap getter ────────────────────────────────────────────────────

  it('giversMap: returns object keyed by id', () => {
    const store = giversStoreObj()
    store.givers = [{ ...mockGiver }]

    expect(store.giversMap['giver-uuid-1']).toEqual(mockGiver)
  })
})
