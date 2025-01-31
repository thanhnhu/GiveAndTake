//import Cookies from 'js-cookie'
import { userStoreObj } from '@/stores/users'

export const headers = () => {
  let data = {
    'Content-Type': 'application/json',
    //'X-CSRFToken': Cookies.get('csrftoken')
  };

  // Using Pinia store for Vue 3
  const userStore = userStoreObj()
  if (userStore.token) {
    data.Authorization = `Token ${userStore.token}`
  }

  return { headers: data };
}