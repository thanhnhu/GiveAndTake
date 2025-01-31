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
        <giver-info />
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
            <th scope="col" class="column-action" v-if="givers.some(r => r.can_edit)">{{ $t('common.action') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(giver, index) in givers" :key="index">
            <td scope="row">{{ giver.number }}</td>
            <td class="text-start">{{ giver.name }}</td>
            <td class="text-start">{{ giver.phone }}</td>
            <td class="text-start">{{ giver.address }}</td>
            <td>{{ cityNameById(giver.city) }}</td>
            <td>
              <i class="bi bi-card-text fs-5" v-if="giver.description && giver.description.length > 20"
                v-tooltip="giver.description" />
              <span v-else>{{ giver.description }}</span>
            </td>
            <td>
              <div v-if="giver.images && giver.images.length > 0" @click="openImages(giver.images)">
                <i class="bi bi-eye fs-5" :title="$t('common.viewimages')" />
              </div>
            </td>
            <td class="column-action" v-if="givers.some(r => r.can_edit)">
              <div class="row justify-content-center">
                <div class="mx-2" v-if="giver.can_edit">
                  <file-uploader :id="giver.id" :is-giver="true" />
                </div>
                <div class="mx-1" v-if="giver.can_edit" @click="setActive(giver.id)">
                  <div v-if="giver.active">
                    <i class="bi bi-stop-circle fs-5" :title="$t('common.stopdonate')" />
                  </div>
                  <div v-else>
                    <i class="bi bi-play-circle fs-5" :title="$t('common.needtodonate')" />
                  </div>
                </div>
                <div class="mx-1" v-if="giver.can_delete">
                  <i class="bi bi-x-circle fs-5 text-danger" :title="$t('common.delete')"
                    @click="handleDelete(giver.id)" />
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <div v-for="(giver, index) in givers" :key="index">
        <div class="card border-info mb-1">
          <div class="row g-0">
            <div class="col-md-4">
              <img :src="firstImage(giver)" class="img-fluid" alt="">
            </div>
            <div class="col-md-8">
              <div class="card-body">
                <div class="container-fluid">
                  <div class="row align-items-start">
                    #{{ giver.number }}, {{ giver.name }}, {{ giver.address }}
                  </div>
                  <div class="row">
                    <i class="bi bi-telephone fs-5 me-3" v-tooltip="giver.phone" />
                    <i class="bi bi-card-text fs-5 me-3" v-if="giver.description && giver.description.length > 20"
                      v-tooltip="giver.description" />
                    <div v-if="giver.images && giver.images.length > 0" @click="openImages(giver.images)">
                      <i class="bi bi-eye fs-5" :title="$t('common.viewimages')" />
                    </div>
                  </div>
                  <div class="row" v-if="givers.some(r => r.can_edit)">
                    <div class="me-3" v-if="giver.can_edit">
                      <file-uploader :id="giver.id" :is-giver="true" />
                    </div>
                    <div v-if="giver.can_edit" @click="setActive(giver.id)">
                      <div v-if="giver.active">
                        <i class="bi bi-stop-circle fs-5" :title="$t('common.stopdonate')" />
                      </div>
                      <div v-else>
                        <i class="bi bi-play-circle fs-5" :title="$t('common.needtodonate')" />
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

    <modal-slider :show="showGiverImages" @close="showGiverImages = false" :images="giverImages" />
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';
import { userStoreObj } from '@/stores/users';
import { citiesStoreObj } from '@/stores/cities';
import { giversStoreObj } from '@/stores/givers';
//import GiverInfo from "@/components/Givers/GiverInfo";
//import ModalDialog from "@/components/ModalDialog";
//import FileUploader from "@/components/FileUploader";
//import ModalSlider from "@/components/ModalSlider";
import { isMobile } from "@/helpers";

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
}</style>
