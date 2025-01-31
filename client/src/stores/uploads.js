import { defineStore } from 'pinia'
import { uploadService } from '@/services/uploadService'
import { giversStoreObj } from '@/stores/givers'
import { takersStoreObj } from '@/stores/takers'

export const uploadsStoreObj = defineStore('uploads', {
  state: () => ({
    fetchingData: false,
    error: null,
    files: []
  }),

  actions: {
    async uploadFiles(data) {
      this.fetchingData = true
      this.error = null
      
      try {
        const images = await uploadService.uploadFiles(data)
        this.fetchingData = false
        
        if (images.length > 0) {
          const key = images[0].key
          if (key) {
            const takersStore = takersStoreObj()
            const giversStore = giversStoreObj()
            
            const takerIndex = takersStore.takers.findIndex(r => r.id === key)
            if (takerIndex >= 0) {
              takersStore.takers[takerIndex].images ??= []
              takersStore.takers[takerIndex].images.push(...images)
            } else {
              const giverIndex = giversStore.givers.findIndex(r => r.id === key)
              giversStore.givers[giverIndex].images ??= []
              giversStore.givers[giverIndex].images.push(...images)
            }
          }
        }
      } catch (error) {
        this.fetchingData = false
        this.error = error
      }
    },

    async downloadFiles() {
      this.fetchingData = true
      this.error = null
      
      try {
        const files = await uploadService.downloadFiles()
        this.fetchingData = false
        this.files = files
      } catch (error) {
        this.fetchingData = false
        this.error = error
        this.files = null
      }
    }
  }
}) 