import api from '@/services/api'
import { headers } from './headers'

export default {
  uploadFiles(files) {
    let header = headers()
    header.headers["Content-Type"] = "multipart/form-data"
    return api.post(`images/`, files, header)
      .then(response => response.data)
  },
  downloadFiles() {
    return api.get(`images/`)
      .then(response => response.data)
  }
}