<script setup>
import axios from 'axios';
import { ref, computed } from 'vue';
import { i18n } from '@/lang/i18n';
import { uploadsStoreObj } from '@/stores/uploads';
import { userStoreObj } from '@/stores/users';
import { headers } from '@/services/headers';
import ModalDialog from '@/components/ModalDialog.vue';

// Props definition
const props = defineProps({
  id: { default: "" },
  isTaker: { default: false },
  isGiver: { default: false },
  parentHandler: { default: false },
  url: {
    type: String,
    default: '/api/images/'
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
const showError = ref(0);
const fileInput = ref(null);

// Computed properties
const user = computed(() => usersStore.user);
const fetchingData = computed(() => uploadsStore.fetchingData);
const error = computed(() => uploadsStore.error);
const useManagedUpload = computed(() => !!props.id);

// Methods
const addFiles = () => {
  fileInput.value.click();
};

const submitFiles = async (closeAfterSave = false) => {
  if (props.parentHandler) {
    emit("onSubmitFiles");
    if (closeAfterSave) showUpload.value = false;
    return;
  }

  if (!files.value.length) {
    showError.value = 5;
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

  await uploadsStore.uploadFiles(formData);
  if (!uploadsStore.error) {
    showSuccess.value = 5;
    files.value = [];
    if (closeAfterSave) showUpload.value = false;
  } else {
    showError.value = 5;
  }
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

const openUploader = () => {
  showError.value = 0;
  showSuccess.value = 0;
  if (useManagedUpload.value) showUpload.value = true;
  else triggerFileInput();
};

const onInputChange = (event) => {
  if (useManagedUpload.value) {
    onFilesChange();
    return;
  }
  handleFileChange(event);
};

const handleFileChange = async (event) => {
  const files = event.target.files;
  if (!files.length) return;

  showError.value = 0;
  showSuccess.value = 0;

  try {
    for (let file of files) {
      if (file.size > props.maxSize) {
        throw new Error(t('upload.fileTooLarge'));
      }

      const formData = new FormData();
      formData.append('files', file);

      const response = await axios.post(props.url, formData, {
        headers: {
          ...headers().headers,
          'Content-Type': 'multipart/form-data'
        }
      });

      const uploaded = Array.isArray(response.data) ? response.data : [response.data];
      uploaded.forEach((img) => emit('upload-success', img));
    }
  } catch (err) {
    showError.value = err.message || t('upload.popup_failed');
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
    <input type="file" ref="fileInput" :accept="accept" multiple @change="onInputChange"
      style="display: none" />
    <button v-if="user" type="button" class="icon-action" :title="t('upload.addnew')" @click="openUploader">
      <i class="bi bi-camera fs-5"></i>
    </button>

    <modal-dialog :show="showUpload" @close="showUpload = false">
      <template #header>{{ t('upload.popup_header') }}</template>
      <template #body>
        <div v-if="showError > 0" class="alert alert-danger py-1 mb-2">{{ t('upload.popup_failed') }}</div>
        <div v-if="showSuccess > 0" class="alert alert-success py-1 mb-2">{{ t('upload.popup_success') }}</div>
        <div class="mb-2 text-center">
          <button type="button" class="btn btn-sm btn-outline-primary" @click="addFiles">
            {{ t('upload.popup_addmore') }}
          </button>
        </div>
        <ul v-if="files.length > 0" class="list-group list-group-flush">
          <li class="list-group-item d-flex justify-content-between align-items-center px-0" v-for="(file, index) in files" :key="index">
            <span class="file-listing">{{ file.name }}</span>
            <button type="button" class="btn btn-sm btn-outline-danger rounded-circle p-0 ms-2 lh-1" style="width:1.4rem;height:1.4rem;font-size:1.1rem" :title="t('common.delete')" @click="removeFile(index)">
              <i class="bi bi-x"></i>
            </button>
          </li>
        </ul>
      </template>
      <template #footer>
        <b-button size="sm" variant="outline-primary" class="me-2" :disabled="fetchingData" @click="submitFiles(true)">
          {{ t('upload.popup_upload') }}
        </b-button>
      </template>
    </modal-dialog>
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
  vertical-align: middle;
  line-height: 1;

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