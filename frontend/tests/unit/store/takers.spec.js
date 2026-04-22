import { setActivePinia, createPinia } from 'pinia'
import { takersStoreObj } from '@/stores/takers'
import takerService from '@/services/takerService'
import { flushPromises } from '@vue/test-utils'

jest.mock('@/services/takerService')

const mockTaker = {
  id: 'uuid-1',
  number: 1,
  name: 'Test Taker',
  phone: '0900000001',
  address: 'Hà Nội',
  city: 1,
  description: '',
  images: [],
  donates: [],
  stop_donate: false,
  can_edit: true,
  can_delete: false,
}

const mockDonate = {
  id: 'donate-uuid-1',
  taker: 'uuid-1',
  user: 1,
  donate: 500000,
  description: 'Test donate',
  date_created: '2026-01-01T00:00:00Z',
}

describe('Takers Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    jest.clearAllMocks()
  })

  // ─── getTakers ───────────────────────────────────────────────────────────

  it('getTakers: populates takers and total on success', async () => {
    const store = takersStoreObj()
    takerService.fetchTakers.mockResolvedValue({ results: [mockTaker], count: 1 })

    await store.getTakers()
    await flushPromises()

    expect(store.takers).toEqual([mockTaker])
    expect(store.total).toBe(1)
    expect(store.fetchingData).toBe(false)
    expect(store.error).toBeNull()
  })

  it('getTakers: sets error and clears takers on failure', async () => {
    const store = takersStoreObj()
    const err = new Error('Network error')
    takerService.fetchTakers.mockRejectedValue(err)

    await store.getTakers()
    await flushPromises()

    expect(store.takers).toEqual([])
    expect(store.error).toBe(err)
    expect(store.fetchingData).toBe(false)
  })

  // ─── addTaker ────────────────────────────────────────────────────────────

  it('addTaker: prepends server response to takers array', async () => {
    const store = takersStoreObj()
    store.takers = [{ ...mockTaker, id: 'uuid-0' }]
    const newTaker = { ...mockTaker, id: 'uuid-new', number: 2 }
    takerService.postTaker.mockResolvedValue(newTaker)

    await store.addTaker({ name: 'New', phone: '09', city: 1, address: 'HN', description: '' })
    await flushPromises()

    expect(store.takers[0]).toEqual(newTaker)
    expect(store.takers).toHaveLength(2)
    expect(store.fetchingData).toBe(false)
  })

  it('addTaker: sets error on failure', async () => {
    const store = takersStoreObj()
    const err = new Error('Server error')
    takerService.postTaker.mockRejectedValue(err)

    await store.addTaker({ name: 'X' })
    await flushPromises()

    expect(store.error).toBe(err)
    expect(store.fetchingData).toBe(false)
  })

  // ─── updateTaker ─────────────────────────────────────────────────────────

  it('updateTaker: replaces taker in array with server response', async () => {
    const store = takersStoreObj()
    store.takers = [{ ...mockTaker }]
    const updated = { ...mockTaker, name: 'Updated Name' }
    takerService.updateTaker.mockResolvedValue(updated)

    await store.updateTaker({ ...mockTaker, name: 'Updated Name' })
    await flushPromises()

    expect(store.takers[0].name).toBe('Updated Name')
    expect(store.fetchingData).toBe(false)
  })

  // ─── removeTaker ─────────────────────────────────────────────────────────

  it('removeTaker: removes taker from array', async () => {
    const store = takersStoreObj()
    store.takers = [{ ...mockTaker }]
    takerService.removeTaker.mockResolvedValue({})

    await store.removeTaker('uuid-1')
    await flushPromises()

    expect(store.takers).toHaveLength(0)
  })

  it('removeTaker: sets error on failure', async () => {
    const store = takersStoreObj()
    store.takers = [{ ...mockTaker }]
    const err = new Error('Delete failed')
    takerService.removeTaker.mockRejectedValue(err)

    await store.removeTaker('uuid-1')
    await flushPromises()

    expect(store.error).toBe(err)
    expect(store.takers).toHaveLength(1)
  })

  // ─── stopDonate ──────────────────────────────────────────────────────────

  it('stopDonate: toggles stop_donate flag', async () => {
    const store = takersStoreObj()
    store.takers = [{ ...mockTaker, stop_donate: false }]
    takerService.stopDonate.mockResolvedValue({})

    await store.stopDonate('uuid-1')
    await flushPromises()

    expect(store.takers[0].stop_donate).toBe(true)
  })

  it('stopDonate: toggles stop_donate back to false', async () => {
    const store = takersStoreObj()
    store.takers = [{ ...mockTaker, stop_donate: true }]
    takerService.stopDonate.mockResolvedValue({})

    await store.stopDonate('uuid-1')
    await flushPromises()

    expect(store.takers[0].stop_donate).toBe(false)
  })

  // ─── addDonate ───────────────────────────────────────────────────────────

  it('addDonate: pushes server response into taker donates', async () => {
    const store = takersStoreObj()
    store.takers = [{ ...mockTaker, donates: [] }]
    takerService.addDonate.mockResolvedValue(mockDonate)

    await store.addDonate({ taker: 'uuid-1', donate: 500000, description: 'Test' })
    await flushPromises()

    expect(store.takers[0].donates).toHaveLength(1)
    expect(store.takers[0].donates[0]).toEqual(mockDonate)
    expect(store.takers[0].donates[0].date_created).toBeDefined()
  })

  it('addDonate: does NOT push request payload (no date_created on payload)', async () => {
    const store = takersStoreObj()
    store.takers = [{ ...mockTaker, donates: [] }]
    takerService.addDonate.mockResolvedValue(mockDonate)

    const payload = { taker: 'uuid-1', donate: 500000, description: 'Test' }
    await store.addDonate(payload)
    await flushPromises()

    // Must use server response, not payload
    expect(store.takers[0].donates[0].id).toBe('donate-uuid-1')
    expect(store.takers[0].donates[0].date_created).toBe('2026-01-01T00:00:00Z')
  })

  it('addDonate: sets error on failure', async () => {
    const store = takersStoreObj()
    store.takers = [{ ...mockTaker, donates: [] }]
    const err = new Error('Donate failed')
    takerService.addDonate.mockRejectedValue(err)

    await store.addDonate({ taker: 'uuid-1', donate: 500000 })
    await flushPromises()

    expect(store.error).toBe(err)
    expect(store.takers[0].donates).toHaveLength(0)
  })

  // ─── updateDonate ────────────────────────────────────────────────────────

  it('updateDonate: replaces donate in taker donates array', async () => {
    const store = takersStoreObj()
    store.takers = [{ ...mockTaker, donates: [{ ...mockDonate }] }]
    takerService.updateDonate.mockResolvedValue({})

    await store.updateDonate({ ...mockDonate, donate: 999999 })
    await flushPromises()

    expect(store.takers[0].donates[0].donate).toBe(999999)
  })

  // ─── removeDonate ────────────────────────────────────────────────────────

  it('removeDonate: removes donate from taker donates array', async () => {
    const store = takersStoreObj()
    store.takers = [{ ...mockTaker, donates: [{ ...mockDonate }] }]
    takerService.removeDonate.mockResolvedValue({})

    await store.removeDonate('donate-uuid-1')
    await flushPromises()

    expect(store.takers[0].donates).toHaveLength(0)
  })

  it('removeDonate: sets error on failure', async () => {
    const store = takersStoreObj()
    store.takers = [{ ...mockTaker, donates: [{ ...mockDonate }] }]
    const err = new Error('Remove failed')
    takerService.removeDonate.mockRejectedValue(err)

    await store.removeDonate('donate-uuid-1')
    await flushPromises()

    expect(store.error).toBe(err)
    expect(store.takers[0].donates).toHaveLength(1)
  })

  // ─── takersMap getter ────────────────────────────────────────────────────

  it('takersMap: returns object keyed by id', async () => {
    const store = takersStoreObj()
    store.takers = [{ ...mockTaker }]

    expect(Object.values(store.takersMap)).toContainEqual(expect.objectContaining({ id: 'uuid-1' }))
  })
})
