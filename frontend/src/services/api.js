import axios from 'axios'

const instance = axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {
    "Content-Type": "application/json"
  }
})

instance.interceptors.request.use(
  config => {
    // Add any auth headers or other request processing here
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

instance.interceptors.response.use(
  response => {
    return response.data // Directly return the data for easier consumption
  },
  error => {
    const errorMessage = error.response?.data?.message || error.message
    console.error('API Error:', errorMessage)
    
    // You can handle specific error codes here
    if (error.response?.status === 401) {
      // Handle unauthorized - could dispatch to auth store
      // Example: router.push('/login')
    }
    
    return Promise.reject({
      message: errorMessage,
      status: error.response?.status,
      originalError: error
    })
  }
)

export default instance