import router from '@/router'
import { toastMessage } from '../../helpers'
import userService from '../../services/userService'
import * as types from './mutation-types'

export default {
  login({ commit }, { username, password }) {
    commit(types.LOGIN_REQUEST, { username })

    userService.login(username, password)
      .then(response => {
        commit(types.LOGIN_SUCCESS, response.data)
        router.push('/')
        toastMessage(`Đăng nhập thành công!`)
      })
      .catch(error => {
        commit(types.LOGIN_FAILURE, { error })
      })
  },
  logout({ dispatch, commit }) {
    commit(types.LOGOUT)
    router.push("/", () => { })
    dispatch('takers/getTakers', null, { root: true })
  },
  //register({ dispatch, commit }, user) {
  register({ commit }, user) {
    commit(types.REGISTER_REQUEST, user)

    userService.register(user)
      .then(user => {
        commit(types.REGISTER_SUCCESS, user)
        router.push('/login')
        toastMessage(`Đăng ký thành công!`)
      })
      .catch(error => {
        commit(types.REGISTER_FAILURE, error)
      })
  },
}
