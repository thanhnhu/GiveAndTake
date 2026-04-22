import * as types from './mutation-types'
import uploadService from '../../services/uploadService'

export default {
  uploadFiles({ commit }, data) {
    commit(types.UPLOAD_FILES_REQUEST)
    uploadService.uploadFiles(data)
      .then(images => { commit(types.UPLOAD_FILES_SUCCESS, images) })
      .catch(error => commit(types.UPLOAD_FILES_FAILURE, { error }))
  },
  downloadFiles({ commit }) {
    commit(types.DOWNLOAD_FILES_REQUEST)

    uploadService.downloadFiles()
      .then(files => commit(types.DOWNLOAD_FILES_SUCCESS, files))
      .catch(error => commit(types.DOWNLOAD_FILES_FAILURE, { error }))
  },
}
