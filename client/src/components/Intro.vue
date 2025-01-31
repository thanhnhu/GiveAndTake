<template>
  <div class="my-2 text-left col-offset-1 col-md-10">
    <h4>{{ $t('intro.intro1') }}</h4>
    <b-row class="mx-4">
      <b-img fluid v-bind:src="isWeb ? '/static/web_children.png' : '/static/mob_children.png'" />
    </b-row>
    <h4 class="mt-2">{{ $t('intro.intro2') }}</h4>
    <br />
    <h4>{{ $t('intro.intro3') }}</h4>
  </div>
</template>

<script>
import { computed } from 'vue';
import { isMobile } from "../helpers";

export default {
  name: "intro",
  setup() {
    const isWeb = computed(() => !isMobile());

    return {
      isWeb
    };
  }
};
</script>

<style lang="scss" scoped></style>
