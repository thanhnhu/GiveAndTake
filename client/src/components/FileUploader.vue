<script setup>
import { ref, computed } from 'vue';
import { uploadsStoreObj } from '@/stores/uploads';
import { userStoreObj } from '@/stores/users';
import ModalDialog from "@/components/ModalDialog.vue";
import { i18n } from '@/lang/i18n';
import axios from 'axios';

// Props definition
const props = defineProps({
  id: { default: "" },
  isTaker: { default: false },
  isGiver: { default: false },
  parentHandler: { default: false },
  url: {
    type: String,
    required: true
  },
  accept: {
    type: String,
    default: 'image/*'
  },
  multiple: {
    type: Boolean,
    default: false
  },
  buttonText: {
    type: String,
    default: ''
  },
  maxSize: {
    type: Number,
    default: 5 * 1024 * 1024 // 5MB
  }
});

// Emit definition
const emit = defineEmits(['upload-success', 'upload-error', 'onSubmitFiles']);

// Store initialization
const uploadsStore = uploadsStoreObj();
const usersStore = userStoreObj();
const t = i18n.global.t;

// Refs
const files = ref([]);
const showUpload = ref(false);
const showSuccess = ref(0);
const showError = ref(false);
const fileInput = ref(null);

// Computed properties
const user = computed(() => usersStore.user);
const fetchingData = computed(() => uploadsStore.fetchingData);
const error = computed(() => uploadsStore.error);

// Methods
const addFiles = () => {
  fileInput.value.click();
};

const submitFiles = () => {
  if (props.parentHandler) {
    emit("onSubmitFiles");
    return;
  }

  let formData = new FormData();
  files.value.forEach((file) => {
    formData.append("files", file);
  });
  formData.append("id", props.id);

  if (props.isGiver) {
    formData.append("isGiver", props.isGiver);
  } else {
    formData.append("isTaker", props.isTaker);
  }

  uploadsStore.uploadFiles(formData);
  files.value = [];
};

const onFilesChange = () => {
  let uploadedFiles = fileInput.value.files;

  for (var i = 0; i < uploadedFiles.length; i++) {
    files.value.push(uploadedFiles[i]);
  }
};

const removeFile = (index) => {
  files.value.splice(index, 1);
};

const onOverlayHidden = () => {
  if (error.value) {
    showError.value = 5;
  } else {
    showSuccess.value = 5;
  }
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileChange = async (event) => {
  const files = event.target.files;
  if (!files.length) return;

  showError.value = '';
  showSuccess.value = 0;

  try {
    for (let file of files) {
      if (file.size > props.maxSize) {
        throw new Error(t('common.fileTooLarge'));
      }

      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(props.url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      emit('upload-success', response.data);
    }
  } catch (err) {
    showError.value = err.message || t('common.uploadError');
    emit('upload-error', err);
  } finally {
    showSuccess.value = 5;
    // Reset the input
    event.target.value = '';
  }
};
</script>

<template>
  <div class="file-uploader">
    <input type="file" ref="fileInput" :accept="accept" :multiple="multiple" @change="handleFileChange"
      style="display: none" />
    <div v-if="user" @click="showUpload = true">
      <!-- <font-awesome-icon icon="camera" :title="t('upload.addnew')" /> -->
      <i class="bi bi-house-door"></i>
      <!-- <font-awesome-icon :icon="['fas', 'camera']" class="fs-5" scale="1.5" :title="t('upload.addnew')" /> -->
      <!-- <b-icon icon="camera" scale="1.5" :title="t('upload.addnew')" /> -->
    </div>
    <!-- <button v-if="user" class="btn btn-primary" @click="triggerFileInput">
      {{ buttonText || t('upload.addnew') }}
    </button> -->
    <div v-if="error" class="error-message text-danger">
      {{ error }}
    </div>
    <div v-if="showSuccess > 0" class="upload-status">
      {{ t('upload.popup_success') }}
    </div>
    <div v-if="showError > 0" class="upload-status">
      {{ t('upload.popup_failed') }}
    </div>
  </div>
</template>

<style>
input[type="file"] {
  position: absolute;
  top: -500px;
}

.file-listing {
  word-break: break-all;
  word-wrap: break-word;
}

.file-error {
  color: red;
}

.file-uploader {
  display: inline-block;
  margin: 10px 0;

  .error-message {
    margin-top: 5px;
    font-size: 0.9em;
  }

  .upload-status {
    margin-top: 5px;
    font-size: 0.9em;
    color: #666;
  }
}
</style>