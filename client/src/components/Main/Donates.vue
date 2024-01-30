<template src="./donates.html"></template>

<script>
import { vue } from '@/main';
import { mapState, mapActions } from "vuex";
import DonateInfo from "@/components/Main/DonateInfo";
import { isMobile } from "../../helpers";

export default {
  name: "donate-list",
  components: { DonateInfo },

  data() {
    return {
      page: 0,
      page_size: 0,
      showAddDonate: false,
    };
  },
  props: ["takerId"],

  computed: {
    ...mapState("users", ["user"]),
    ...mapState("takers", ["takers", "fetchingData", "error"]),
    isWeb() {
      return !isMobile();
    },

    taker() {
      let index = this.takers.findIndex((r) => r.id === this.takerId);
      return index >= 0 ? this.takers[index] : {};
    },

    start() {
      return (this.page - 1) * this.page_size;
    },
    end() {
      return this.page * this.page_size;
    },
    rows() {
      return this.taker.donates.length;
    },
  },

  methods: {
    ...mapActions("takers", ["addDonate", "updateDonate", "removeDonate"]),

    handleDelete(donateId) {
      let res = confirm(vue.$i18n.t('common.confirmDelete'));
      if (res) {
        this.removeDonate(donateId);
      }
    },

    initPaging() {
      this.page = 1;
      this.page_size = this.isWeb ? 15 : 7;
    },
  },

  created() {
    this.paging = this.initPaging();
  },
};
</script>

<style lang="scss" scoped>
.column-date {
  width: 10rem;
}

.column-donate {
  width: 10rem;
}

.column-desc {
  width: auto;
}

.column-action {
  width: 6rem;
}
</style>