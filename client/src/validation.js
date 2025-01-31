import { configure, defineRule } from 'vee-validate'
import { required, email } from '@vee-validate/rules'
import { app } from '@/main'

// Define validation rules
defineRule('required', required)
defineRule('email', email)

// Configure global validation settings
configure({
  generateMessage: (context) => {
    const { field } = context
    //return app.config.globalProperties.$i18n.t('common.field_required', { field })
    return `The ${field} field is required`
  }
})