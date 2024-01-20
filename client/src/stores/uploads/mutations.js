import * as types from './mutation-types'
import store from '../../stores'

export default {
  [types.UPLOAD_FILES_REQUEST](state) {
    state.fetchingData = true
    state.error = null
  },
  [types.UPLOAD_FILES_SUCCESS](state, images) {
    state.fetchingData = false
    state.error = null

    if (images.length > 0) {
      let key = images[0].key
      if (key) {
        let index = store.state.takers.takers.findIndex(r => r.id === key)
        if (index >= 0) {
          store.state.takers.takers[index].images = store.state.takers.takers[index].images || []
          store.state.takers.takers[index].images.push(...images)
        } else {
          index = store.state.givers.givers.findIndex(r => r.id === key)
          store.state.givers.givers[index].images = store.state.givers.givers[index].images || []
          store.state.givers.givers[index].images.push(...images)
        }
      }
    }
  },
  [types.UPLOAD_FILES_FAILURE](state, { error }) {
    state.fetchingData = false
    state.error = error
  },

  [types.DOWNLOAD_FILES_REQUEST](state) {
    state.fetchingData = true
    state.error = null
  },
  [types.DOWNLOAD_FILES_SUCCESS](state, files) {
    state.fetchingData = false
    state.error = null
    state.files = files
  },
  [types.DOWNLOAD_FILES_FAILURE](state, { error }) {
    state.fetchingData = false
    state.error = error
    state.files = null
  },
}
