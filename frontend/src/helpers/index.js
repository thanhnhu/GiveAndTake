import { useToast } from "vue-toastification";

export const toastMessage = (message) => {
  const toast = useToast()
  toast.info(message, {
    timeout: 5000
  })
}

const SERVER_ERROR_KEYS = {
  'Unable to log in with provided credentials.': 'errors.invalid_credentials',
  'A user with that username already exists.': 'errors.username_exists',
  'Not found': 'errors.not_found',
  'Permission denied': 'errors.permission_denied',
}

export const translateError = (message, t, te) => {
  if (!message) return ''
  const key = SERVER_ERROR_KEYS[message]
  if (key && te(key)) return t(key)
  return message
}

export const arrayToObject = (array, keyField) => {
  if (!array) return {}
  return array.reduce((obj, item) => {
    obj[item[keyField]] = item
    return obj
  }, {})
}

export const arrayOrderedToObject = (array, keyField) => {
  if (!array) return {}
  return array.reduce((obj, item, index) => {
    obj[`${index}_${item[keyField]}`] = item
    return obj
  }, {})
}

export const isMobile = () => {
  if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    return true
  } else {
    return false
  }
}
