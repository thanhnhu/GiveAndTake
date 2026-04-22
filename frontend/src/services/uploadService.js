import api from '@/services/api'
import { headers } from '@/services/headers'

export default {
  async uploadFiles(files) {
    try {
      let header = headers()
      header.headers['Content-Type'] = null  // Override instance default; lets axios auto-detect FormData and set multipart boundary
      header.timeout = 1000 * 60 * 5  // 5m for large files
      return await api.post('images/', files, header)
    } catch (error) {
      console.error('Error uploading files:', error)
      throw error
    }
  },

  async downloadFiles() {
    try {
      return await api.get('images/')
    } catch (error) {
      console.error('Error downloading files:', error)
      throw error
    }
  }
}