import { createBootstrap } from 'bootstrap-vue-next';
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faHandHoldingHeart, faEye } from '@fortawesome/free-solid-svg-icons'
import Toast from 'vue-toastification'

// Importing styles
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'
import 'vue-toastification/dist/index.css'
import "@/assets/styles/global.css"

export default function installBootstrap(app) {
  // Setup Font Awesome
  library.add(faHandHoldingHeart, faEye)
  app.component('font-awesome-icon', FontAwesomeIcon)
  
  // Setup Bootstrap Vue Next
  app.use(createBootstrap());

  app.use(Toast);
}