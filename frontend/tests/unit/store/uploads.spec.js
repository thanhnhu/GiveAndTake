import { setActivePinia, createPinia } from 'pinia'
import { uploadsStoreObj } from '@/stores/uploads'
import { takersStoreObj } from '@/stores/takers'
import { giversStoreObj } from '@/stores/givers'
import uploadService from '@/services/uploadService'
import { flushPromises } from '@vue/test-utils'

jest.mock('@/services/uploadService')
jest.mock('@/services/takerService')
jest.mock('@/services/giverService')

const mockImage = { key: 'taker-uuid-1', url: 'http://example.com/img.jpg', mob_url: 'http://example.com/img-mob.jpg' }

describe('Uploads Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    jest.clearAllMocks()
  })

  // ─── uploadFiles ─────────────────────────────────────────────────────────

  it('uploadFiles: pushes images to matching taker', async () => {
    const store = uploadsStoreObj()
    const takersStore = takersStoreObj()
    takersStore.takers = [{ id: 'taker-uuid-1', images: [] }]

    uploadService.uploadFiles.mockResolvedValue([mockImage])

    await store.uploadFiles(new FormData())
    await flushPromises()

    expect(takersStore.takers[0].images).toHaveLength(1)
    expect(takersStore.takers[0].images[0]).toEqual(mockImage)
    expect(store.fetchingData).toBe(false)
    expect(store.error).toBeNull()
  })

  it('uploadFiles: pushes images to matching giver when not found in takers', async () => {
    const store = uploadsStoreObj()
    const takersStore = takersStoreObj()
    const giversStore = giversStoreObj()
    takersStore.takers = []
    giversStore.givers = [{ id: 'giver-uuid-1', images: [] }]

    uploadService.uploadFiles.mockResolvedValue([{ ...mockImage, key: 'giver-uuid-1' }])

    await store.uploadFiles(new FormData())
    await flushPromises()

    expect(giversStore.givers[0].images).toHaveLength(1)
  })

  it('uploadFiles: initializes images array if null', async () => {
    const store = uploadsStoreObj()
    const takersStore = takersStoreObj()
    takersStore.takers = [{ id: 'taker-uuid-1', images: null }]

    uploadService.uploadFiles.mockResolvedValue([mockImage])

    await store.uploadFiles(new FormData())
    await flushPromises()

    expect(takersStore.takers[0].images).toHaveLength(1)
  })

  it('uploadFiles: does nothing when image key is empty', async () => {
    const store = uploadsStoreObj()
    const takersStore = takersStoreObj()
    takersStore.takers = [{ id: 'taker-uuid-1', images: [] }]

    uploadService.uploadFiles.mockResolvedValue([{ ...mockImage, key: '' }])

    await store.uploadFiles(new FormData())
    await flushPromises()

    expect(takersStore.takers[0].images).toHaveLength(0)
  })

  it('uploadFiles: sets error on failure', async () => {
    const store = uploadsStoreObj()
    const err = new Error('Upload failed')
    uploadService.uploadFiles.mockRejectedValue(err)

    await store.uploadFiles(new FormData())
    await flushPromises()

    expect(store.error).toBe(err)
    expect(store.fetchingData).toBe(false)
  })

  // ─── downloadFiles ───────────────────────────────────────────────────────

  it('downloadFiles: populates files on success', async () => {
    const store = uploadsStoreObj()
    const files = [{ id: 1, url: 'http://example.com/a.jpg' }]
    uploadService.downloadFiles.mockResolvedValue(files)

    await store.downloadFiles()
    await flushPromises()

    expect(store.files).toEqual(files)
    expect(store.fetchingData).toBe(false)
    expect(store.error).toBeNull()
  })

  it('downloadFiles: sets error on failure', async () => {
    const store = uploadsStoreObj()
    const err = new Error('Download failed')
    uploadService.downloadFiles.mockRejectedValue(err)

    await store.downloadFiles()
    await flushPromises()

    expect(store.error).toBe(err)
    expect(store.fetchingData).toBe(false)
  })
})
