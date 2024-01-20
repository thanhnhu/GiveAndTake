<template src="./givers.html"></template>

<script>
import { mapState, mapActions } from "vuex";
import GiverInfo from "@/components/Givers/GiverInfo";
import ModalDialog from "@/components/ModalDialog";
import FileUploader from "@/components/FileUploader";
import ModalSlider from "@/components/ModalSlider";
import { isMobile } from "../../helpers";

export default {
  name: "givers",
  components: { GiverInfo, ModalDialog, FileUploader, ModalSlider },

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
      giverImages: {},
      showGiverImages: false,
    };
  },

  computed: {
    ...mapState("users", ["user"]),
    ...mapState("cities", ["cities"]),
    ...mapState("givers", ["total", "givers", "fetchingData", "error"]),
    isWeb() {
      return !isMobile();
    },
  },

  methods: {
    ...mapActions("cities", ["getCities"]),
    ...mapActions("givers", ["getGivers", "setActive", "removeGiver"]),

    openImages(images) {
      this.giverImages = images;
      this.showGiverImages = true;
    },

    firstImage(giver) {
      if (giver.images && giver.images.length > 0) {
        return giver.images[0].mob_url;
      }
      return "/static/user.png";
    },

    cityNameById(id) {
      let index = this.cities.findIndex((r) => r.id === id);
      return index >= 0 ? this.cities[index].name : "";
    },

    handleDelete(giverId) {
      let res = confirm("Bạn có chắc chắn xóa?");
      if (res) {
        this.removeGiver(giverId);
      }
    },

    cityChange(cityName) {
      let index = this.cities.findIndex((r) => r.name === cityName);
      if (index >= 0) {
        let city = this.cities[index].id;
        let filter = this.buildFilterParams(city);
        this.getGivers(filter);
      } else {
        let filter = this.buildFilterParams(true);
        this.getGivers(filter);
      }
    },
    isMineChange() {
      this.filter.isMine = !this.filter.isMine;
      let filter = this.buildFilterParams(null, this.filter.isMine);
      this.getGivers(filter);
    },
    filterChange() {
      let filter = this.buildFilterParams(null, null, true);
      this.getGivers(filter);
    },
    pagingChange(value) {
      let filter = this.buildFilterParams(null, null, null, value);
      this.getGivers(filter);
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
    this.getGivers(filter);
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
  max-width: 4rem;
}

.card-img-left {
  height: 10rem;
  width: 10rem;
}

.align-items-start {
  text-align: left;
  word-break: break-all;
}
</style>
