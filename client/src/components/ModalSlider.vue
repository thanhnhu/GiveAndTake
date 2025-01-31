<script>
import { ref, computed, onMounted, watch } from 'vue';
import { isMobile } from "@/helpers";

export default {
  name: "modal-slider",
  props: {
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
  },
  emits: ['close', 'update:show'],
  setup(props, { emit }) {
    const localShow = ref(props.show);
    const activeIndex = ref(0);
    const sliding = ref(false);

    const currentImg = computed(() => {
      let curIndex = Math.abs(activeIndex.value) % props.images.length;
      return isMobile()
        ? props.images[curIndex].mob_url
        : props.images[curIndex].web_url;
    });

    const startSlide = () => {
      timer.value = setInterval(next, 5000);
    };

    const next = () => {
      activeIndex.value += 1;
    };

    const prev = () => {
      activeIndex.value -= 1;
    };

    const close = () => {
      emit("close");
    };

    const onSlideStart = () => {
      sliding.value = true;
    };

    const onSlideEnd = () => {
      sliding.value = false;
    };

    const onHidden = () => {
      activeIndex.value = 0;
    };

    const timer = ref(null);

    watch(() => props.show, (newVal) => {
      localShow.value = newVal;
    });

    watch(() => localShow.value, (newVal) => {
      emit('update:show', newVal);
    });

    onMounted(() => {
      startSlide();
    });

    return {
      localShow,
      activeIndex,
      sliding,
      currentImg,
      next,
      prev,
      close,
      onSlideStart,
      onSlideEnd,
      onHidden
    };
  }
};
</script>

<template>
  <b-modal
    v-model="localShow"
    size="xl"
    :title="title"
    hide-footer
    @hidden="onHidden"
  >
    <div class="modal-slider">
      <b-carousel
        v-model="activeIndex"
        :interval="0"
        controls
        indicators
        img-width="100%"
        img-height="480"
        @sliding-start="onSlideStart"
        @sliding-end="onSlideEnd"
      >
        <b-carousel-slide
          v-for="(image, index) in images"
          :key="index"
          :img-src="image.url"
        />
      </b-carousel>
    </div>
  </b-modal>
</template>

<style lang="scss" scoped>
.modal-slider {
  .carousel-item {
    img {
      object-fit: contain;
      width: 100%;
      height: 480px;
    }
  }
}
</style>