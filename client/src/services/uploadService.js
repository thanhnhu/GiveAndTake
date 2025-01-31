import api from '@/services/api'
import { headers } from '@/services/headers'

export const uploadService = () => {
  const uploadFiles = async (files) => {
    try {
      let header = headers()
      header.headers["Content-Type"] = "multipart/form-data"
      header.timeout = 1000 * 60 * 5  // 5m for large files
      const response = await api.post('images/', files, header)
      return response.data
    } catch (error) {
      console.error('Error uploading files:', error)
      throw error
    }
  }

  const downloadFiles = async () => {
    try {
      const response = await api.get('images/')
      return response.data
    } catch (error) {
      console.error('Error downloading files:', error)
      throw error
    }
  }

  return {
    uploadFiles,
    downloadFiles
  }
}