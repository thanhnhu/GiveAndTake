<template src="./main.html"></template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useI18n } from 'vue-i18n'
import { userStoreObj } from '@/stores/users'
import { citiesStoreObj } from '@/stores/cities'
import { takersStoreObj } from '@/stores/takers'
import { isMobile } from "@/helpers"
import FileUploader from "@/components/FileUploader.vue"
import ModalSlider from "@/components/ModalSlider.vue"
import TakerInfo from "@/components/Main/TakerInfo.vue"
import DonateInfo from "@/components/Main/DonateInfo.vue"

const { t } = useI18n()
const userStore = userStoreObj()
const citiesStore = citiesStoreObj()
const takersStore = takersStoreObj()

// Reactive refs
const paging = ref({})
const filter = ref({
  city: "",
  isMine: false,
  number: "",
  name: "",
  phone: "",
})
const takerImages = ref({})
const showTakerImages = ref(false)

// Store refs
const { user } = storeToRefs(userStore)
const { cities, optionCities } = storeToRefs(citiesStore)
const { takers, total, fetchingData, error } = storeToRefs(takersStore)

// Computed
const isWeb = computed(() => !isMobile())

// Methods
const totalDonate = (taker) => {
  if (taker.donates)
    return taker.donates.reduce((total, item) => total + item.donate, 0)
  return 0
}

const openImages = (images) => {
  takerImages.value = images
  showTakerImages.value = true
}

const cityNameById = (id) => {
  let index = cities.value.findIndex((r) => r.id === id)
  return index >= 0 ? cities.value[index].name : ""
}

const firstImage = (taker) => {
  if (taker.images && taker.images.length > 0) {
    return taker.images[0].mob_url
  }
  return "/assets/user.png"
}

const handleDelete = (takerId) => {
  let res = confirm(t('common.confirmDelete'))
  if (res) {
    takersStore.removeTaker(takerId)
  }
}

const stopDonate = (takerId) => {
  takersStore.stopDonate(takerId)
}

const cityChange = (cityName) => {
  let index = cities.value.findIndex((r) => r.name === cityName)
  if (index >= 0) {
    let city = cities.value[index].id
    let filterParams = buildFilterParams(city)
    takersStore.getTakers(filterParams)
  } else {
    let filterParams = buildFilterParams(true)
    takersStore.getTakers(filterParams)
  }
}

const isMineChange = () => {
  filter.value.isMine = !filter.value.isMine
  let filterParams = buildFilterParams(null, filter.value.isMine)
  takersStore.getTakers(filterParams)
}

const filterChange = () => {
  let filterParams = buildFilterParams(null, null, true)
  takersStore.getTakers(filterParams)
}

const pagingChange = (value) => {
  let filterParams = buildFilterParams(null, null, null, value)
  takersStore.getTakers(filterParams)
}

const buildFilterParams = (city, isMine, filterFlag, page) => {
  if (city) {
    paging.value = initPaging()
    filter.value.city = city
    if (city === true) delete filter.value.city
    delete filter.value.number
    delete filter.value.name
    delete filter.value.phone
  } else if (isMine === true || isMine === false) {
    paging.value = initPaging()
    delete filter.value.number
    delete filter.value.name
    delete filter.value.phone
  } else if (filterFlag) {
    paging.value = initPaging()
  } else if (page) {
    return { ...filter.value, ...paging.value, page }
  }
  return { ...filter.value, ...paging.value }
}

const initPaging = () => {
  return { page_size: isWeb.value ? 20 : 10, page: 1 }
}

// Lifecycle hooks
onMounted(() => {
  citiesStore.getCities()
  paging.value = initPaging()
  let filterParams = buildFilterParams()
  takersStore.getTakers(filterParams)
})
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
  word-wrap: break-word;
}

</style>
