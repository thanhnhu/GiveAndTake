<script setup>
import { computed, ref, watch, onUnmounted } from 'vue'
import { isMobile } from '@/helpers'

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: ''
  },
  images: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'update:show'])

const localShow = ref(props.show)
const currentIndex = ref(0)
const timer = ref(null)
const previousBodyOverflow = ref('')
const previousHtmlOverflow = ref('')

const normalizedIndex = computed(() => {
  const total = props.images?.length || 0
  if (!total) return 0
  return ((currentIndex.value % total) + total) % total
})

const currentImg = computed(() => {
  const total = props.images?.length || 0
  if (!total) return ''
  return getImageSrc(props.images[normalizedIndex.value])
})

const hasMultipleImages = computed(() => (props.images?.length || 0) > 1)

const startSlide = () => {
  if (timer.value || !hasMultipleImages.value) return
  timer.value = setInterval(next, 5000)
}

const stopSlide = () => {
  if (timer.value) {
    clearInterval(timer.value)
    timer.value = null
  }
}

const setScrollLock = (locked) => {
  if (locked) {
    previousBodyOverflow.value = document.body.style.overflow
    previousHtmlOverflow.value = document.documentElement.style.overflow
    document.body.style.overflow = 'hidden'
    document.documentElement.style.overflow = 'hidden'
    return
  }

  document.body.style.overflow = previousBodyOverflow.value
  document.documentElement.style.overflow = previousHtmlOverflow.value
}

const next = () => { currentIndex.value += 1 }
const prev = () => { currentIndex.value -= 1 }
const close = () => {
  localShow.value = false
  emit('close')
}

const handleKeydown = (event) => {
  if (!localShow.value) return
  if (event.key === 'ArrowRight') next()
  if (event.key === 'ArrowLeft') prev()
  if (event.key === 'Escape') close()
}

const getImageSrc = (image) => {
  if (!image) return ''
  if (image.url) return image.url
  return isMobile() ? (image.mob_url || image.web_url || '') : (image.web_url || image.mob_url || '')
}

watch(() => props.show, (newVal) => {
  localShow.value = newVal
})

watch(() => localShow.value, (newVal) => {
  emit('update:show', newVal)
  setScrollLock(newVal)
  if (newVal) {
    startSlide()
    window.addEventListener('keydown', handleKeydown)
    return
  }

  stopSlide()
  window.removeEventListener('keydown', handleKeydown)
  currentIndex.value = 0
})

onUnmounted(() => {
  stopSlide()
  setScrollLock(false)
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <Transition name="modal">
    <div v-if="localShow" class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <button type="button" class="btn-close" @click="close">x</button>

            <TransitionGroup name="fade" tag="div" class="v-middle">
              <div class="v-middle" v-for="i in [currentIndex]" :key="i">
                <img v-if="currentImg" :src="currentImg" :alt="`slide-${normalizedIndex}`" class="slider-image" />
              </div>
            </TransitionGroup>

            <a v-if="hasMultipleImages" class="prev" @click.prevent="prev" href="#">&#10094; &#10094;</a>
            <a v-if="hasMultipleImages" class="next" @click.prevent="next" href="#">&#10095; &#10095;</a>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style lang="scss" scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  overflow: hidden;
  height: 100%;
}

.modal-dialog {
  max-width: 100vw;
  width: 100vw;
  height: 100vh;
  margin: 0;
  display: flex;
}

.modal-content {
  background-color: transparent;
  transition: opacity 0.3s ease;
  border: 0;
  border-radius: 0;
  width: 100%;
  height: 100%;
}

.v-middle {
  position: relative;
  top: 50%;
  transform: translateY(-50%);
}

.slider-image {
  max-height: 96vh;
  max-width: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.9s ease;
  overflow: hidden;
  visibility: visible;
  position: absolute;
  width: 100%;
  opacity: 1;
}

.fade-enter-from,
.fade-leave-to {
  visibility: hidden;
  width: 100%;
  opacity: 0;
}

.prev,
.next {
  cursor: pointer;
  position: absolute;
  top: 40%;
  width: auto;
  padding: 16px;
  color: #fff;
  font-weight: bold;
  font-size: 18px;
  transition: 0.7s ease;
  border-radius: 0 4px 4px 0;
  text-decoration: none;
  user-select: none;
}

.next {
  right: 0;
}

.prev {
  left: 0;
}

.prev:hover,
.next:hover {
  background-color: rgba(0, 0, 0, 0.9);
}
</style>