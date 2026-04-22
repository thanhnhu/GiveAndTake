import Vue from 'vue';
import { vue } from '@/main';
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate';
import { required, email } from "vee-validate/dist/rules";

Vue.component('ValidationProvider', ValidationProvider);
Vue.component('ValidationObserver', ValidationObserver);

extend('required', {
  ...required,
  message: (name) => vue.$i18n.t('common.field_required', { field: name })
});
extend('email', {
  ...email,
  message: (name) => vue.$i18n.t('common.field_invalid', { field: name })
});