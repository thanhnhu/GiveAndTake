import { useToast } from "vue-toastification";
const toast = useToast()

export const toastMessage = (message) => {
  //app.config.globalProperties.$bvToast.toast(message, {
  toast.info(message, {
    autoHideDelay: 5000
  })
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
