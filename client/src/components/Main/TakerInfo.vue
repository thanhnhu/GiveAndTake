<template>
  <div class="taker-info">
    <b-modal
      v-model="localShow"
      :title="$t('taker.info')"
      size="lg"
      hide-footer
      @hidden="onHidden"
    >
      <b-form @submit.prevent="handleSubmit" v-if="!fetchingData">
        <b-form-group :label="$t('taker.number')">
          <b-form-input
            v-model="form.number"
            type="text"
            required
            :placeholder="$t('taker.numberPlaceholder')"
          />
        </b-form-group>

        <b-form-group :label="$t('taker.name')">
          <b-form-input
            v-model="form.name"
            type="text"
            required
            :placeholder="$t('taker.namePlaceholder')"
          />
        </b-form-group>

        <b-form-group :label="$t('taker.phone')">
          <b-form-input
            v-model="form.phone"
            type="text"
            required
            :placeholder="$t('taker.phonePlaceholder')"
          />
        </b-form-group>

        <b-form-group :label="$t('taker.city')">
          <b-form-select
            v-model="form.city"
            :options="optionCities"
            required
          />
        </b-form-group>

        <b-form-group :label="$t('taker.address')">
          <b-form-textarea
            v-model="form.address"
            rows="3"
            required
            :placeholder="$t('taker.addressPlaceholder')"
          />
        </b-form-group>

        <b-form-group :label="$t('taker.description')">
          <b-form-textarea
            v-model="form.description"
            rows="3"
            required
            :placeholder="$t('taker.descriptionPlaceholder')"
          />
        </b-form-group>

        <file-uploader
          :url="uploadUrl"
          multiple
          @upload-success="handleUploadSuccess"
          @upload-error="handleUploadError"
        />

        <div v-if="form.images && form.images.length" class="image-preview">
          <div v-for="(image, index) in form.images" :key="index" class="image-item">
            <img :src="image.mob_url" :alt="image.name" />
            <button class="btn btn-danger btn-sm" @click="removeImage(index)">
              {{ $t('common.remove') }}
            </button>
          </div>
        </div>

        <div class="mt-3">
          <b-button type="submit" variant="primary" :disabled="submitting">
            {{ $t('common.submit') }}
          </b-button>
        </div>
      </b-form>
      <div v-else class="text-center">
        <b-spinner variant="primary" />
      </div>
    </b-modal>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useI18n } from 'vue-i18n'
import { takersStoreObj } from '@/stores/takers'
import { citiesStoreObj } from '@/stores/cities'
import FileUploader from '@/components/FileUploader.vue'

const { t } = useI18n()
const takersStore = takersStoreObj()
const citiesStore = citiesStoreObj()

// Props
const props = defineProps({
  show: Boolean,
  taker: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['update:show'])

// Store refs
const { fetchingData } = storeToRefs(takersStore)
const { optionCities } = storeToRefs(citiesStore)

// Refs
const localShow = ref(props.show)
const submitting = ref(false)
const form = ref({
  number: '',
  name: '',
  phone: '',
  city: '',
  address: '',
  description: '',
  images: []
})

// Computed
const uploadUrl = computed(() => `${process.env.VUE_APP_API_URL}/api/images/`)

// Watchers
watch(() => props.show, (newVal) => {
  localShow.value = newVal
})

watch(() => localShow.value, (newVal) => {
  emit('update:show', newVal)
})

watch(() => props.taker, (newVal) => {
  if (newVal && Object.keys(newVal).length) {
    form.value = { ...newVal }
  }
}, { immediate: true })

// Methods
const handleSubmit = async () => {
  submitting.value = true
  try {
    if (props.taker.id) {
      await takersStore.updateTaker({ ...form.value, id: props.taker.id })
    } else {
      await takersStore.createTaker(form.value)
    }
    localShow.value = false
  } catch (error) {
    console.error('Submit error:', error)
  } finally {
    submitting.value = false
  }
}

const handleUploadSuccess = (response) => {
  if (!form.value.images) {
    form.value.images = []
  }
  form.value.images.push(response)
}

const handleUploadError = (error) => {
  console.error('Upload error:', error)
}

const removeImage = (index) => {
  form.value.images.splice(index, 1)
}

const onHidden = () => {
  form.value = {
    number: '',
    name: '',
    phone: '',
    city: '',
    address: '',
    description: '',
    images: []
  }
}
</script>

<style lang="scss" scoped>
.image-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;

  .image-item {
    position: relative;
    width: 100px;

    img {
      width: 100%;
      height: 100px;
      object-fit: cover;
    }

    button {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      font-size: 0.8rem;
    }
  }
}
</style>