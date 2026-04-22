import { app } from '@/main'
import moment from 'moment'

app.config.globalProperties.$filters = {
  formatDate(value) {
    if (value) {
      return moment(String(value)).format('YYYY/MM/DD HH:mm')
    }
  }
}