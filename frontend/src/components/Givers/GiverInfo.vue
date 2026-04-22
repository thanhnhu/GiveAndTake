<template src="./giverInfo.html"></template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useForm, useField } from 'vee-validate'
import { useI18n } from 'vue-i18n'
import * as yup from 'yup'
import { userStoreObj } from '@/stores/users'
import { citiesStoreObj } from '@/stores/cities'
import { giversStoreObj } from '@/stores/givers'
import ModalDialog from "@/components/ModalDialog.vue"

// Store initialization
const userStore = userStoreObj()
const citiesStore = citiesStoreObj()
const giversStore = giversStoreObj()
const { t } = useI18n()

// Store refs
const { user } = storeToRefs(userStore)
const { fetchingData, error } = storeToRefs(giversStore)
const { optionCities } = storeToRefs(citiesStore)

const observerGiver = ref(null)
const showAddGiver = ref(false)

// Form validation schema (computed to react to locale changes)
const validationSchema = computed(() => yup.object({
  name: yup.string().required(t('common.field_required', { field: t('common.fullname') })),
  phone: yup.string().required(t('common.field_required', { field: t('common.phone') })),
  address: yup.string().required(t('common.field_required', { field: t('common.address') })),
  city: yup.number().nullable().required(t('common.field_required', { field: t('common.city') })),
  description: yup.string()
}))

watch(showAddGiver, (val) => { if (val) resetForm() })

// Initialize form with vee-validate
const { handleSubmit, resetForm } = useForm({
  validationSchema,
  initialValues: {
    name: "",
    phone: "",
    address: "",
    city: null,
    description: ""
  }
})

// Create validated fields
const { value: name, errorMessage: nameError } = useField('name')
const { value: phone, errorMessage: phoneError } = useField('phone')
const { value: address, errorMessage: addressError } = useField('address')
const { value: city, errorMessage: cityError } = useField('city')
const { value: description } = useField('description')

// Methods
const handleSaveGiver = handleSubmit(async (values) => {
  await giversStore.addGiver(values)
  resetForm()
  observerGiver.value?.reset()
})

const handleSaveAndClose = handleSubmit(async (values) => {
  await giversStore.addGiver(values)
  resetForm()
  observerGiver.value?.reset()
  showAddGiver.value = false
})

// Fetch cities when component mounts
onMounted(() => {
  citiesStore.getCities()
})
</script>