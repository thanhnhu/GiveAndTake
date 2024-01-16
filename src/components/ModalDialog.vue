<script>
export default {
  name: "modal-dialog",
  props: {
    show: {
      default: false,
    },
  },
  methods: {
    close() {
      this.$emit("close");
    },
  },
};
</script>

<template>
  <div v-if="show">
    <transition name="modal">
      <div class="modal-mask">
        <div class="modal-wrapper">
          <div
            class="modal-dialog"
            role="document"
            aria-labelledby="modalTitle"
            aria-describedby="modalDescription"
          >
            <div class="modal-content">
              <header class="modal-header" id="modalTitle">
                <slot name="header"> This is the default tile! </slot>
                <button
                  type="button"
                  class="btn-close"
                  @click="close"
                  aria-label="Close modal"
                >
                  x
                </button>
              </header>

              <section class="modal-body" id="modalDescription">
                <slot name="body"> This is the default body! </slot>
              </section>

              <footer class="modal-footer">
                <slot name="footer"> This is the default footer! </slot>
                <b-button size="sm" variant="outline-secondary" @click="close"
                  >Bỏ qua</b-button
                >
              </footer>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  overflow: auto;
  justify-content: center;
  vertical-align: middle;
}

.modal-header,
.modal-footer {
  padding: 10px;
  display: flex;
}

.modal-header {
  position: relative;
  border-bottom: 1px solid #eeeeee;
  color: #4aae9b;
  justify-content: space-between;
}

.modal-footer {
  border-top: 1px solid #eeeeee;
  flex-direction: row;
}

.modal-body {
  position: relative;
  padding: 20px 10px;
}

.modal-fade-enter,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.5s ease;
}
</style>