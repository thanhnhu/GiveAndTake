import { configure, defineRule } from 'vee-validate'
import { required, email } from '@vee-validate/rules'
import { i18n } from '@/lang/i18n'

// Define validation rules
defineRule('required', required)
defineRule('email', email)

// Configure global validation settings
configure({
  generateMessage: (context) => {
    const { field, rule } = context
    if (rule.name === 'email') {
      return i18n.global.t('common.field_invalid', { field })
    }
    return i18n.global.t('common.field_required', { field })
  }
})