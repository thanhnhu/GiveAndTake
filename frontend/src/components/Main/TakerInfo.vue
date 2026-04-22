<template src="./takerInfo.html"></template>

<script setup>
import { ref, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useForm, useField } from 'vee-validate'
import { useI18n } from 'vue-i18n'
import * as yup from 'yup'
import { takersStoreObj } from '@/stores/takers'
import { citiesStoreObj } from '@/stores/cities'
import { userStoreObj } from '@/stores/users'
import ModalDialog from '@/components/ModalDialog.vue'

const { t } = useI18n()
const takersStore = takersStoreObj()
const citiesStore = citiesStoreObj()
const usersStore = userStoreObj()

// Store refs
const { fetchingData } = storeToRefs(takersStore)
const { cities } = storeToRefs(citiesStore)
const { user } = storeToRefs(usersStore)

const showAddTaker = ref(false)

// Form validation schema (computed to react to locale changes)
const validationSchema = computed(() => yup.object({
  name: yup.string().required(t('common.field_required', { field: t('common.fullname') })),
  phone: yup.string().required(t('common.field_required', { field: t('common.phone') })),
  address: yup.string().required(t('common.field_required', { field: t('common.address') })),
  city: yup.number().nullable().required(t('common.field_required', { field: t('common.city') })),
  description: yup.string()
}))

// Initialize form with vee-validate
watch(showAddTaker, (val) => { if (val) resetForm() })

const { handleSubmit, resetForm } = useForm({
  validationSchema,
  initialValues: {
    name: '',
    phone: '',
    address: '',
    city: null,
    description: ''
  }
})

// Create validated fields
const { value: name, errorMessage: nameError } = useField('name')
const { value: phone, errorMessage: phoneError } = useField('phone')
const { value: address, errorMessage: addressError } = useField('address')
const { value: city, errorMessage: cityError } = useField('city')
const { value: description } = useField('description')

const handleSave = handleSubmit(async (values) => {
  await takersStore.addTaker(values)
  resetForm()
})

const handleSaveAndClose = handleSubmit(async (values) => {
  await takersStore.addTaker(values)
  resetForm()
  showAddTaker.value = false
})
</script>