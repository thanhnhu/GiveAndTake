<script>
import { isMobile } from "@/helpers";

export default {
  name: "modal-slider",
  data() {
    return {
      timer: null,
      currentIndex: 0,
    };
  },

  props: {
    show: {
      default: false,
    },
    images: [],
  },

  computed: {
    currentImg: function () {
      let curIndex = Math.abs(this.currentIndex) % this.images.length;
      return isMobile()
        ? this.images[curIndex].mob_url
        : this.images[curIndex].web_url;
    },
  },

  mounted: function () {
    this.startSlide();
  },

  methods: {
    startSlide: function () {
      this.timer = setInterval(this.next, 5000);
    },

    next: function () {
      this.currentIndex += 1;
    },
    prev: function () {
      this.currentIndex -= 1;
    },

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
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <button type="button" class="btn-close" @click="close()">
                x
              </button>

              <transition-group name="fade" tag="div" class="v-middle">
                <div class="v-middle" v-for="i in [currentIndex]" :key="i">
                  <b-img fluid :src="currentImg"></b-img>
                </div>
              </transition-group>
              <a class="prev" @click="prev" href="#">&#10094; &#10094;</a>
              <a class="next" @click="next" href="#">&#10095; &#10095;</a>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style lang="scss" scoped>
.modal-dialog {
  max-width: 100%;
  margin: 0;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100vh;
  display: flex;
}

.modal-content {
  background-color: transparent;
  transition: opacity 0.3s ease;
}

.v-middle {
  position: relative;
  top: 50%;
  transform: translateY(-50%);
}

img {
  max-height: 96vh;
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

.fade-enter,
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
  color: white;
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