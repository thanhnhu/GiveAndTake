import { setActivePinia, createPinia } from 'pinia'
import { markRaw } from 'vue'
import { userStoreObj } from '@/stores/users'
import userService from '@/services/userService'
import { flushPromises } from '@vue/test-utils'

jest.mock('@/services/userService')

describe('User Store', () => {
  let mockRouter

  beforeEach(() => {
    mockRouter = { push: jest.fn() }
    setActivePinia(createPinia())
    jest.clearAllMocks()
  })

  it('sets token and user on successful login', async () => {
    const userStore = userStoreObj()
    userStore.router = markRaw(mockRouter)

    userService.login.mockResolvedValue({
      token: 'test-token',
      user: JSON.stringify({ id: 1, username: 'testuser' })
    })

    await userStore.login({ username: 'testuser', password: 'password' })
    await flushPromises()

    expect(userStore.token).toBe('test-token')
    expect(userStore.user).toEqual({ id: 1, username: 'testuser' })
    expect(userStore.error).toBeNull()
    expect(userStore.fetchingData).toBe(false)
  })

  it('sets error on failed login', async () => {
    const userStore = userStoreObj()

    const loginError = new Error('Invalid credentials')
    userService.login.mockRejectedValue(loginError)

    await userStore.login({ username: 'bad', password: 'bad' })
    await flushPromises()

    expect(userStore.token).toBeNull()
    expect(userStore.user).toBeNull()
    expect(userStore.error).toBe(loginError)
    expect(userStore.fetchingData).toBe(false)
  })

  it('clears token and user on logout', () => {
    const userStore = userStoreObj()
    userStore.router = markRaw(mockRouter)
    userStore.token = 'some-token'
    userStore.user = { id: 1, username: 'testuser' }

    userStore.logout()

    expect(userStore.token).toBeNull()
    expect(userStore.user).toBeNull()
  })

  it('navigates to /login after successful registration', async () => {
    const userStore = userStoreObj()
    userStore.router = markRaw(mockRouter)

    userService.register.mockResolvedValue({})

    await userStore.register({ username: 'newuser', password: 'pass', email: 'a@b.com' })
    await flushPromises()

    expect(userStore.fetchingData).toBe(false)
    expect(userStore.error).toBeNull()
  })
})