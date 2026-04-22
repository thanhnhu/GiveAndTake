<template src="./givers.html"></template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';
import { userStoreObj } from '@/stores/users';
import { citiesStoreObj } from '@/stores/cities';
import { giversStoreObj } from '@/stores/givers';
import { isMobile } from "@/helpers";
import GiverInfo from "@/components/Givers/GiverInfo.vue";
import FileUploader from "@/components/FileUploader.vue";
import ModalSlider from "@/components/ModalSlider.vue";

const giversStore = giversStoreObj();
const citiesStore = citiesStoreObj();
const usersStore = userStoreObj();
const { t } = useI18n();

const {
  givers,
  total,
  fetchingData,
  error
} = storeToRefs(giversStore);

const { cities } = storeToRefs(citiesStore);
const { user } = storeToRefs(usersStore);

const paging = ref({});
const filter = ref({
  city: "",
  isMine: false,
  number: "",
  name: "",
  phone: "",
});
const giverImages = ref({});
const showGiverImages = ref(false);

// Computed properties
const isWeb = computed(() => !isMobile());

// Methods
const openImages = (images) => {
  giverImages.value = images;
  showGiverImages.value = true;
};

const firstImage = (giver) => {
  if (giver.images && giver.images.length > 0) {
    return giver.images[0].mob_url;
  }
  return "/static/user.png";
};

const cityNameById = (id) => {
  let index = cities.value.findIndex((r) => r.id === id);
  return index >= 0 ? cities.value[index].name : "";
};

const handleDelete = (giverId) => {
  let res = confirm(t('common.confirmDelete'));
  if (res) {
    giversStore.removeGiver(giverId);
  }
};

const initPaging = () => {
  return { page_size: isWeb.value ? 20 : 10, page: 1 };
};

const buildFilterParams = (city, isMine, filterParam, page) => {
  if (city) {
    paging.value = initPaging();
    filter.value.city = city;
    if (city === true) delete filter.value.city;
    delete filter.value.number;
    delete filter.value.name;
    delete filter.value.phone;
  } else if (isMine === true || isMine === false) {
    paging.value = initPaging();
    delete filter.value.number;
    delete filter.value.name;
    delete filter.value.phone;
  } else if (filterParam) {
    paging.value = initPaging();
  } else if (page) {
    return { ...filter.value, ...paging.value, page };
  }
  return { ...filter.value, ...paging.value };
};

const cityChange = (cityName) => {
  let index = cities.value.findIndex((r) => r.name === cityName);
  if (index >= 0) {
    let city = cities.value[index].id;
    let filterParams = buildFilterParams(city);
    giversStore.getGivers(filterParams);
  } else {
    let filterParams = buildFilterParams(true);
    giversStore.getGivers(filterParams);
  }
};

const isMineChange = () => {
  filter.value.isMine = !filter.value.isMine;
  let filterParams = buildFilterParams(null, filter.value.isMine);
  giversStore.getGivers(filterParams);
};

const filterChange = () => {
  let filterParams = buildFilterParams(null, null, true);
  giversStore.getGivers(filterParams);
};

const pagingChange = (value) => {
  let filterParams = buildFilterParams(null, null, null, value);
  giversStore.getGivers(filterParams);
};

const setActive = (id) => giversStore.setActive(id);

onMounted(() => {
  citiesStore.getCities();
  paging.value = initPaging();
  let filterParams = buildFilterParams();
  giversStore.getGivers(filterParams);
});
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
  width: 10%;
  white-space: nowrap;
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
