<script>
import { mapState, mapActions } from "vuex";
import ModalDialog from "@/components/ModalDialog";

export default {
  name: "file-uploader",
  components: { ModalDialog },

  data() {
    return {
      files: [],
      showUpload: false,
      showSuccess: 0,
      showError: 0,
    };
  },

  props: {
    id: { default: "" },
    isTaker: { default: false },
    isGiver: { default: false },
    parentHandler: { default: false },
  },

  computed: {
    ...mapState("users", ["user"]),
    ...mapState("uploads", ["fetchingData", "error"]),
  },

  methods: {
    ...mapActions("uploads", ["uploadFiles"]),
    addFiles() {
      this.$refs.files.click();
    },
    submitFiles() {
      if (this.parentHandler) {
        this.$emit("onSubmitFiles");
        return;
      }

      let formData = new FormData();
      this.files.forEach((file) => {
        formData.append("files", file);
      });
      formData.append("id", this.id);

      if (this.isGiver) {
        formData.append("isGiver", this.isGiver);
      } else {
        formData.append("isTaker", this.isTaker);
      }

      this.uploadFiles(formData);
      this.files = [];
    },

    onFilesChange() {
      let uploadedFiles = this.$refs.files.files;

      for (var i = 0; i < uploadedFiles.length; i++) {
        this.files.push(uploadedFiles[i]);
      }
    },
    removeFile(index) {
      this.files.splice(index, 1);
    },

    onOverlayHidden() {
      if (this.error) {
        this.showError = 5;
      } else {
        this.showSuccess = 5;
      }
    },
  },
};
</script>

<template>
  <div class="">
    <div v-if="user" @click="showUpload = true">
      <b-icon icon="camera" scale="1.5" title="Thêm hình ảnh" />
    </div>

    <modal-dialog :show="showUpload" @close="showUpload = false">
      <template v-slot:header>Thêm hình ảnh (hình không quá 10MB)</template>
      <template v-slot:body>
        <div>
          <b-alert variant="info" dismissible fade :show="showSuccess" @dismissed="showSuccess = 0">
            Tải hình lên thành công!
          </b-alert>
          <b-alert variant="warning" dismissible fade :show="showError" @dismissed="showError = 0">
            Có lỗi khi tải hình!
          </b-alert>
        </div>
        <b-overlay :show="fetchingData" variant="transparent" @hidden="onOverlayHidden">
          <div>
            <input type="file" id="files" ref="files" multiple @change="onFilesChange"
              accept="image/jpeg, image/jpg, image/png, image/gif" />
          </div>
          <b-row v-for="(file, index) in files" :key="index" class="align-middle file-listing">
            <div class="ml-3 mr-2">
              <b-icon icon="x-circle" scale="1.2" variant="danger" title="Xóa" @click="removeFile(index)" />
            </div>
            <div class="mr-2" :class="{ 'file-error': file.size > 1024 * 1024 * 10 }">
              {{ file.name }}
            </div>
          </b-row>
          <div class="mt-1">
            <b-button size="sm" variant="outline-primary" @click="addFiles">Thêm hình</b-button>
          </div>
        </b-overlay>
      </template>
      <template v-slot:footer>
        <b-button size="sm" variant="outline-primary" @click="submitFiles"
          :disabled="fetchingData || !files || files.length == 0">Tải lên</b-button>
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
</style>