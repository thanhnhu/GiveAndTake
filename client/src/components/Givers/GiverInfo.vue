<template>
  <div>
    <button v-if="user" type="button" class="btn btn-sm btn-outline-primary" @click="showAddGiver = true">
      {{ $t('common.addnew') }}
    </button>

    <form @submit.prevent="handleSaveGiver" ref="observerGiver">
      <modal-dialog :show="showAddGiver" @close="showAddGiver = false">
        <template #header>{{ $t('giver.addnew') }}</template>
        <template #body>
          <div class="mb-3">
            <div class="input-group">
              <input type="text" class="form-control" :class="{ 'is-invalid': nameError }" aria-label="fullname"
                :placeholder="$t('common.fullname')" v-model="name" />
            </div>
            <div class="error-messages" v-if="nameError">{{ nameError }}</div>
          </div>

          <div class="mb-3">
            <div class="input-group">
              <input type="text" class="form-control" :class="{ 'is-invalid': phoneError }" aria-label="phone"
                :placeholder="$t('common.phone')" v-model="phone" />
            </div>
            <div class="error-messages" v-if="phoneError">{{ phoneError }}</div>
          </div>

          <div class="mb-3">
            <div class="input-group">
              <input type="text" class="form-control" :class="{ 'is-invalid': addressError }" aria-label="Address"
                maxlength="50" :placeholder="$t('common.address')" v-model="address" />
            </div>
            <div class="error-messages" v-if="addressError">{{ addressError }}</div>
          </div>

          <div class="mb-3">
            <div class="input-group">
              <select class="form-select" :class="{ 'is-invalid': cityError }" v-model="city">
                <option v-for="city in optionCities" :key="city.id" :value="city.id">
                  {{ city.name }}
                </option>
              </select>
            </div>
            <div class="error-messages" v-if="cityError">{{ cityError }}</div>
          </div>

          <div class="input-group">
            <div class="input-group-prepend">
              <span class="input-group-text">{{ $t('common.description') }}</span>
            </div>
            <textarea class="form-control" aria-label="description" v-model="description"></textarea>
          </div>
        </template>
        <template #footer>
          <button type="button" class="btn btn-sm btn-outline-primary" :disabled="fetchingData"
            @click="handleSaveAndClose">{{ $t('common.saveandclose') }}</button>
          <button type="button" class="btn btn-sm btn-outline-primary" @click="handleSaveGiver"
            :disabled="fetchingData">{{ $t('common.save') }}</button>
        </template>
      </modal-dialog>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useForm, useField } from 'vee-validate'
import * as yup from 'yup'
import { userStoreObj } from '@/stores/users'
import { citiesStoreObj } from '@/stores/cities'
import { giversStoreObj } from '@/stores/givers'
import ModalDialog from "@/components/ModalDialog.vue"

// Store initialization
const userStore = userStoreObj()
const citiesStore = citiesStoreObj()
const giversStore = giversStoreObj()

// Store refs
const { user } = storeToRefs(userStore)
const { fetchingData, error } = storeToRefs(giversStore)
const { optionCities } = storeToRefs(citiesStore)

const observerGiver = ref(null)
const showAddGiver = ref(false)

// Form validation schema
const validationSchema = yup.object({
  name: yup.string().required(),
  phone: yup.string().required(),
  address: yup.string().required(),
  city: yup.number().nullable().required(),
  description: yup.string()
})

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