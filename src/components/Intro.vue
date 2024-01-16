<template>
  <div class="my-2 text-left col-offset-1 col-md-10">
    <h4>
      1. Tổng hợp thông tin về những hoành cảnh về người, địa phương khó khăn để
      các nhà hảo tâm, từ thiện có thể đến và giúp đỡ
    </h4>
    <b-row class="mx-4">
      <b-img fluid v-bind:src="isWeb ? '/static/web_children.png' : '/static/mob_children.png'" />
    </b-row>
    <h4 class="mt-2">
      2. Tổng hợp thông tin về những người, đơn vị từ thiện để những hoàn cảnh
      khó khăn có thể liên hệ và được giúp đỡ
    </h4>
    <br />
    <h4>
      3. Kết nối các nhà hảo tâm, tổ chức từ thiện để tạo ra cộng đồng lớn nhằm
      chia sẻ thông tin về các trường hợp khó khăn, các chương trình thiện
      nguyện
    </h4>
  </div>
</template>

<script>
import { isMobile } from "../helpers";

export default {
  name: "intro",
  computed: {
    isWeb: () => {
      return !isMobile();
    },
  },
};
</script>

<style lang="scss" scoped>
</style>
