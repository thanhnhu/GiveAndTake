<template>
  <div class="donate-info">
    <b-modal
      v-model="localShow"
      :title="$t('donate.info')"
      size="lg"
      hide-footer
      @hidden="onHidden"
    >
      <b-form @submit.prevent="handleSubmit" v-if="!fetchingData">
        <b-form-group :label="$t('donate.donate')">
          <b-form-input
            v-model.number="form.donate"
            type="number"
            required
            :placeholder="$t('donate.donatePlaceholder')"
          />
        </b-form-group>

        <b-form-group :label="$t('donate.description')">
          <b-form-textarea
            v-model="form.description"
            rows="3"
            required
            :placeholder="$t('donate.descriptionPlaceholder')"
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
import FileUploader from '@/components/FileUploader.vue'

const { t } = useI18n()
const takersStore = takersStoreObj()

// Props
const props = defineProps({
  show: Boolean,
  takerId: {
    type: String,
    required: true
  },
  donate: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['update:show'])

// Store refs
const { fetchingData } = storeToRefs(takersStore)

// Refs
const localShow = ref(props.show)
const submitting = ref(false)
const form = ref({
  donate: 0,
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

watch(() => props.donate, (newVal) => {
  if (newVal && Object.keys(newVal).length) {
    form.value = { ...newVal }
  }
}, { immediate: true })

// Methods
const handleSubmit = async () => {
  submitting.value = true
  try {
    if (props.donate.id) {
      await takersStore.updateDonate({
        ...form.value,
        id: props.donate.id,
        taker: props.takerId
      })
    } else {
      await takersStore.createDonate({
        ...form.value,
        taker: props.takerId
      })
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
    donate: 0,
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