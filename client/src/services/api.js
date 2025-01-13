import axios from 'axios'

// export default axios.create({
//   baseURL: '/api',
//   timeout: 5000
// })

const instance = axios.create({
  baseURL: '/api',
  timeout: 5000
  // headers: {
  //     Authorization: `Bearer ${token}`
  // }
})

instance.interceptors.request.use(config => {
  //this.cover = true;
  // if (token) {
  //   config.headers.Authorization = `Bearer ${token}`;
  // }
  return config;
}, error => Promise.reject(error));

instance.interceptors.response.use(response => {
  //this.cover = false;
  return response
}, error => {
  //this.cover = false;
  console.log('Exception: ', error)
  //if (error) throw error
  return Promise.reject(error)
});

export default instance;