import { setActivePinia, createPinia } from 'pinia'
import { userStoreObj } from '@/stores/users'
import { userService } from '@/services/userService'
import { flushPromises } from '@vue/test-utils'

jest.mock('@/services/userService')

describe('User Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('updates user profile', async () => {
    const userStore = userStoreObj()
    const mockUserService = userService()

    mockUserService.updateUser.mockResolvedValue({
      id: 1,
      name: 'abc',
      lastName: 'bar'
    })

    expect(userStore.fullName).toBe('')
    
    await userStore.updateProfile({
      name: 'abc',
      lastName: 'bar'
    })

    await flushPromises()
    
    expect(userStore.fullName).toBe('abc bar')
    expect(userStore.error).toBeNull()
  })

  it('handles login', async () => {
    const userStore = userStoreObj()
    const mockUserService = userService()

    mockUserService.login.mockResolvedValue({
      token: 'test-token',
      user: {
        id: 1,
        username: 'testuser'
      }
    })

    await userStore.login({
      username: 'testuser',
      password: 'password'
    })

    expect(userStore.user).toEqual({
      id: 1,
      username: 'testuser'
    })
    expect(userStore.token).toBe('test-token')
  })
})