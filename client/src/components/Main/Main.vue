<template src="./main.html"></template>

<script>
import { vue } from '@/main';
import { mapState, mapActions, mapGetters } from "vuex";
import FileUploader from "@/components/FileUploader";
import ModalSlider from "@/components/ModalSlider";
import TakerInfo from "@/components/Main/TakerInfo";
import DonateInfo from "@/components/Main/DonateInfo";
import { isMobile } from "../../helpers";

export default {
  name: "main-view",
  components: { FileUploader, ModalSlider, TakerInfo, DonateInfo },

  data() {
    return {
      paging: {},
      filter: {
        city: "",
        isMine: false,
        number: "",
        name: "",
        phone: "",
      },
      takerImages: {},
      showTakerImages: false,
    };
  },

  computed: {
    ...mapState("users", ["user"]),
    ...mapState("cities", ["cities"]),
    ...mapState("takers", ["total", "fetchingData", "error"]),
    ...mapGetters("takers", ["takers"]),
    ...mapGetters("cities", ["optionCities"]),
    isWeb() {
      return !isMobile();
    },
  },

  methods: {
    ...mapActions("cities", ["getCities"]),
    ...mapActions("takers", ["getTakers", "stopDonate", "removeTaker"]),

    totalDonate(taker) {
      if (taker.donates)
        return taker.donates.reduce((total, item) => total + item.donate, 0);
      return 0;
    },

    openImages(images) {
      this.takerImages = images;
      this.showTakerImages = true;
    },

    cityNameById(id) {
      let index = this.cities.findIndex((r) => r.id === id);
      return index >= 0 ? this.cities[index].name : "";
    },

    firstImage(taker) {
      if (taker.images && taker.images.length > 0) {
        return taker.images[0].mob_url;
      }
      return "/static/user.png";
    },

    handleDelete(takerId) {
      let res = confirm(vue.$i18n.t('common.confirmDelete'));
      if (res) {
        this.removeTaker(takerId);
      }
    },

    cityChange(cityName) {
      let index = this.cities.findIndex((r) => r.name === cityName);
      if (index >= 0) {
        let city = this.cities[index].id;
        let filter = this.buildFilterParams(city);
        this.getTakers(filter);
      } else {
        let filter = this.buildFilterParams(true);
        this.getTakers(filter);
      }
    },
    isMineChange() {
      this.filter.isMine = !this.filter.isMine;
      let filter = this.buildFilterParams(null, this.filter.isMine);
      this.getTakers(filter);
    },
    filterChange() {
      let filter = this.buildFilterParams(null, null, true);
      this.getTakers(filter);
    },
    pagingChange(value) {
      let filter = this.buildFilterParams(null, null, null, value);
      this.getTakers(filter);
    },
    buildFilterParams(city, isMine, filter, page) {
      if (city) {
        this.paging = this.initPaging();
        this.filter.city = city;
        if (city === true) delete this.filter.city;
        delete this.filter.number;
        delete this.filter.name;
        delete this.filter.phone;
      } else if (isMine === true || isMine === false) {
        this.paging = this.initPaging();
        delete this.filter.number;
        delete this.filter.name;
        delete this.filter.phone;
      } else if (filter) {
        this.paging = this.initPaging();
      } else if (page) {
        return { ...this.filter, ...this.paging, page };
      }
      return { ...this.filter, ...this.paging };
    },
    initPaging() {
      return { page_size: this.isWeb ? 20 : 10, page: 1 };
    },
  },

  created() {
    this.getCities();

    this.paging = this.initPaging();
    let filter = this.buildFilterParams();
    this.getTakers(filter);
  },
};
</script>

<style lang="scss" scoped>
h3 {
  text-align: left;
  margin: 1.5rem;
}

.column-number {
  width: 5rem;
}

.column-name {
  width: 10rem;
}

.column-phone {
  width: 7rem;
}

.column-city {
  width: 12rem;
}

.column-images {
  width: 6rem;
}

.column-action {
  width: auto;
  max-width: 6rem;
}

.card-img-left {
  height: 10rem;
  width: 10rem;
}

.align-items-start {
  text-align: left;
  word-break: break-all;
  word-wrap: break-word;
}
</style>
