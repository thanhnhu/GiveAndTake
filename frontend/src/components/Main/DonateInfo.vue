<template src="./donateInfo.html"></template>

<script setup>
import { ref, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useI18n } from 'vue-i18n'
import { useForm, useField } from 'vee-validate'
import * as yup from 'yup'
import { takersStoreObj } from '@/stores/takers'
import ModalDialog from '@/components/ModalDialog.vue'


const { t } = useI18n()
const takersStore = takersStoreObj()

// Props
const props = defineProps({
  show: Boolean,
  isNewInline: {
    type: Boolean,
    default: false
  },
  isNew: {
    type: Boolean,
    default: false
  },
  isEdit: {
    type: Boolean,
    default: false
  },
  editObject: {
    type: Object,
    default: () => ({})
  },
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

// Validation schema (computed to react to locale changes)
const validationSchema = computed(() => yup.object({
  donate: yup.number()
    .typeError(t('common.field_required', { field: t('donate.money') }))
    .required(t('common.field_required', { field: t('donate.money') }))
    .min(1, t('common.field_invalid', { field: t('donate.money') })),
  description: yup.string()
}))

const { handleSubmit, resetForm } = useForm({ validationSchema, initialValues: { donate: null, description: '' } })
const { value: donateValue, errorMessage: donateError } = useField('donate')
const { value: description } = useField('description')

// Watchers
watch(() => props.show, (newVal) => {
  localShow.value = newVal
})

watch(() => localShow.value, (newVal) => {
  emit('update:show', newVal)
  if (newVal) {
    resetForm()
    const source = props.editObject?.id ? props.editObject : props.donate?.id ? props.donate : null
    if (source) {
      donateValue.value = source.donate
      description.value = source.description
    }
  }
})

watch(() => props.donate, (newVal) => {
  if (newVal && Object.keys(newVal).length) {
    donateValue.value = newVal.donate
    description.value = newVal.description
  }
}, { immediate: true })

watch(() => props.editObject, (newVal) => {
  if (newVal && Object.keys(newVal).length) {
    donateValue.value = newVal.donate
    description.value = newVal.description
  }
}, { immediate: true })

// Methods
const doSave = handleSubmit(async (values) => {
  const editTarget = props.editObject?.id ? props.editObject : props.donate
  if (editTarget?.id) {
    await takersStore.updateDonate({ ...values, id: editTarget.id, taker: props.takerId })
  } else {
    await takersStore.addDonate({ ...values, taker: props.takerId })
  }
})

const handleSaveAndClose = async () => {
  await doSave()
  if (!donateError.value) {
    localShow.value = false
    resetForm()
  }
}

const handleSave = async () => {
  await doSave()
}

const onHidden = () => {
  resetForm()
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