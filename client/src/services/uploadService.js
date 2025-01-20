import api from '@/services/api'
import { headers } from './headers'

export default {
  uploadFiles(files) {
    let header = headers()
    header.headers["Content-Type"] = "multipart/form-data"
    header.timeout= 1000 * 60 * 5  // 5m for large files
    return api.post(`images/`, files, header)
      .then(response => response.data)
      .catch(error => console.log(error))
  },
  downloadFiles() {
    return api.get(`images/`)
      .then(response => response.data)
  }
}