import Vue from 'vue'
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate';
import { required, email } from "vee-validate/dist/rules";
import i18n from '@/lang/i18n.js';

Vue.component('ValidationProvider', ValidationProvider);
Vue.component('ValidationObserver', ValidationObserver);

extend('required', {
  ...required,
  message: (name) => `${i18n.t('common.field_required', { field: name })}`
});
extend('email', {
  ...email,
  message: (name) => `${i18n.t('common.field_invalid', { field: name })}`
});