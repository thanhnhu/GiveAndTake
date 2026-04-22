<template>
  <footer :style="{ position: isWeb ? 'fixed' : 'relative' }">
    <span>💻 with ❤️</span>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { isMobile } from "@/helpers"

const isWeb = computed(() => !isMobile())
</script>

<style lang="scss" scoped>
footer {
  box-sizing: border-box;
  background-color: #cfd8dc;
  bottom: 0;
  left: 0;
  padding: 0.8rem;
  position: absolute;
  width: 100%;
}
</style>
