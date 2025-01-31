<template>
  <div>
    <div class="row">
      <div class="col-12 col-sm-3 mb-2">
        <input class="form-control form-control-sm" list="cityList" :placeholder="$t('common.city')" @change="cityChange"
          @keyup.delete="cityChange">
        <datalist id="cityList">
          <option :key="city.id" :value="city.name" v-for="city in cities" />
        </datalist>
      </div>
      <div class="col">
        <div v-if="fetchingData">{{ $t('common.loading') }}</div>
      </div>
      <div class="col-6 col-sm-4 mb-2 d-flex justify-content-end" v-if="user">
        <taker-info />
        <button class="btn btn-sm ms-2" :class="filter.isMine ? 'btn-secondary' : 'btn-outline-primary'"
          :disabled="fetchingData" @click="isMineChange">{{ $t('common.mine') }}</button>
      </div>
    </div>

    <div v-if="isWeb">
      <table class="table table-sm table-bordered table-striped table-hover">
        <thead>
          <tr>
            <th scope="col" class="column-number">
              <input type="number" class="form-control form-control-sm" v-model="filter.number" min="0" placeholder="#"
                @input="filterChange" />
            </th>
            <th scope="col" class="column-name">
              <input type="text" class="form-control form-control-sm" v-model="filter.name"
                :placeholder="$t('common.fullname')" @input="filterChange" />
            </th>
            <th scope="col" class="column-phone">
              <input type="text" class="form-control form-control-sm" v-model="filter.phone"
                :placeholder="$t('common.phone')" @input="filterChange" />
            </th>
            <th scope="col" class="text-start">{{ $t('common.address') }}</th>
            <th scope="col" class="column-city">{{ $t('common.city') }}</th>
            <th scope="col">{{ $t('common.description') }}</th>
            <th scope="col" class="column-images">{{ $t('common.images') }}</th>
            <th scope="col">{{ $t('common.donate') }}</th>
            <th scope="col" class="column-action">{{ $t('common.action') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(taker, index) in takers" :key="index">
            <td scope="row">{{ taker.number }}</td>
            <td class="text-start">{{ taker.name }}</td>
            <td class="text-start">{{ taker.phone }}</td>
            <td class="text-start">{{ taker.address }}</td>
            <td>{{ cityNameById(taker.city) }}</td>
            <td>
              <i class="bi bi-card-text fs-5" v-if="taker.description && taker.description.length > 20"
                v-tooltip="taker.description" />
              <span v-else>{{ taker.description }}</span>
            </td>
            <td>
              <div v-if="taker.images && taker.images.length > 0" @click="openImages(taker.images)">
                <font-awesome-icon :icon="['fas', 'eye']" class="fs-5" :title="$t('common.viewimages')" />
              </div>
            </td>
            <td>
              <div class="float-end">{{ Number(totalDonate(taker)).toLocaleString() }} vnđ
                <router-link v-if="taker.donates && taker.donates.length > 0"
                  :to="{ name: 'donates', params: { takerId: taker.id } }">
                  <i class="bi bi-layout-text-sidebar fs-5" :title="$t('common.viewdescription')" />
                </router-link>
              </div>
            </td>
            <td class="column-action">
              <div class="row justify-content-center">
                <div class="mx-2" v-if="!taker.stop_donate">
                  <div v-if="user">
                    <donate-info :taker-id="taker.id" :is-new-inline="true" />
                  </div>
                  <div v-else>
                    <i class="bi bi-gift fs-5" :title="$t('common.wannadonate')" />
                  </div>
                </div>
                <div class="mx-1" v-if="taker.can_edit">
                  <file-uploader :id="taker.id" :is-taker="true" />
                </div>
                <div class="mx-2" v-if="taker.can_edit" @click="stopDonate(taker.id)">
                  <div v-if="taker.stop_donate">
                    <i class="bi bi-play-circle fs-5" :title="$t('common.needtodonate')" />
                  </div>
                  <div v-else>
                    <i class="bi bi-stop-circle fs-5" :title="$t('common.stopdonate')" />
                  </div>
                </div>
                <div class="me-2" v-if="taker.can_delete">
                  <i class="bi bi-x-circle fs-5 text-danger" :title="$t('common.delete')"
                    @click="handleDelete(taker.id)" />
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <div v-for="(taker, index) in takers" :key="index">
        <div class="card border-info mb-1">
          <div class="row g-0">
            <div class="col-4">
              <img :src="firstImage(taker)" class="img-fluid rounded-start" :alt="taker.name">
            </div>
            <div class="col-8">
              <div class="card-body">
                <div class="container-fluid">
                  <div class="row align-items-start">
                    #{{ taker.number }}, {{ taker.name }}, {{ taker.address }}
                  </div>
                  <div class="row">
                    <i class="bi bi-telephone me-3 mb-1" v-tooltip="taker.phone" />
                    <i class="bi bi-card-text me-3 fs-5" v-if="taker.description && taker.description.length > 20"
                      v-tooltip="taker.description" />
                    <div v-if="taker.images && taker.images.length > 0" @click="openImages(taker.images)">
                      <i class="bi bi-eye fs-5" :title="$t('common.viewimages')" />
                    </div>
                  </div>
                  <div class="row align-items-start" v-if="!taker.stop_donate">
                    <div v-if="user">
                      <donate-info :taker-id="taker.id" :is-new-inline="true" />
                    </div>
                    <div v-else>
                      <i class="bi bi-gift fs-5" :title="$t('common.needtodonate')" />
                    </div>
                    <div class="ms-2">{{ totalDonate(taker) }} vnđ</div>
                  </div>
                  <div class="row">
                    <div class="me-3" v-if="taker.can_edit">
                      <file-uploader :id="taker.id" :is-taker="true" />
                    </div>
                    <div class="me-3" v-if="taker.can_edit" @click="stopDonate(taker.id)">
                      <div v-if="taker.stop_donate">
                        <i class="bi bi-play-circle fs-5" :title="$t('common.needtodonate')" />
                      </div>
                      <div v-else>
                        <i class="bi bi-stop-circle fs-5" :title="$t('common.stopdonate')" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <nav v-if="total > paging.page_size" class="mt-2 d-flex justify-content-center">
      <ul class="pagination">
        <li class="page-item" :class="{ disabled: paging.page === 1 }">
          <a class="page-link" href="#" @click.prevent="pagingChange(paging.page - 1)">Previous</a>
        </li>
        <li class="page-item" v-for="n in Math.ceil(total / paging.page_size)" :key="n"
          :class="{ active: paging.page === n }">
          <a class="page-link" href="#" @click.prevent="pagingChange(n)">{{ n }}</a>
        </li>
        <li class="page-item" :class="{ disabled: paging.page === Math.ceil(total / paging.page_size) }">
          <a class="page-link" href="#" @click.prevent="pagingChange(paging.page + 1)">Next</a>
        </li>
      </ul>
    </nav>

    <modal-slider :show="showTakerImages" @close="showTakerImages = false" :images="takerImages" />
  </div>
</template>

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
