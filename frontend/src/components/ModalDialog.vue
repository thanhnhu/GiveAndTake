<script setup>
const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}
</script>

<template>
  <Transition name="modal">
    <div v-if="show" class="modal-mask" @click.self="close">
      <div class="modal-wrapper">
        <div class="modal-dialog" role="document" aria-labelledby="modalTitle" aria-describedby="modalDescription">
          <div class="modal-content">
            <header class="modal-header" id="modalTitle">
              <slot name="header"> This is the default tile! </slot>
              <button type="button" class="btn-close" @click="close" aria-label="Close modal">x</button>
            </header>

            <section class="modal-body" id="modalDescription">
              <slot name="body"> This is the default body! </slot>
            </section>

            <footer class="modal-footer">
              <slot name="footer"> This is the default footer! </slot>
              <b-button size="sm" variant="outline-secondary" @click="close">{{ $t('common.cancel') }}</b-button>
            </footer>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
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
  display: table-cell;
  vertical-align: top;
  padding-top: 60px;
}

.modal-dialog {
  max-width: 500px;
  margin: 0 auto;
}

.modal-content {
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  background-color: #fff;
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