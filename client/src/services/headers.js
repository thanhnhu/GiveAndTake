
//import Cookies from 'js-cookie'
import store from '../stores'

export const headers = () => {
  let data = {
    'Content-Type': 'application/json',
    //'X-CSRFToken': Cookies.get('csrftoken')
  };

  // this store working along with vuex-persistedstate
  if (store.state.users.token) {
    data.Authorization = `Token ${store.state.users.token}`
  }

  return { headers: data };
}