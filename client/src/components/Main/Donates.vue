<template>
  <div>
    <div class="row mb-2">
      <div class="col">
        <div v-if="fetchingData">{{ $t('common.loading') }}</div>
      </div>
      <div class="col-5 col-sm-4 d-flex justify-content-end" v-if="user">
        <donate-info :taker-id="takerId" :is-new="true" />
      </div>
    </div>

    <div v-if="isWeb">
      <table class="table table-sm table-bordered table-striped table-hover">
        <thead>
          <tr>
            <th scope="col" class="column-date">{{ $t('common.createddate') }}</th>
            <th scope="col" class="column-donate">{{ $t('common.donate') }}</th>
            <th scope="col" class="column-desc">{{ $t('common.description') }}</th>
            <th scope="col" v-if="taker.can_edit" class="column-action">{{ $t('common.action') }}</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(donate, index) in taker.donates" :key="index">
            <tr v-if="start <= index && index < end">
              <td scope="row" class="column-date">{{ formatDate(donate.date_created) }}</td>
              <td class="column-donate">
                <div class="float-right">{{ Number(donate.donate).toLocaleString() }} vnđ</div>
              </td>
              <td class="column-desc">{{ donate.description }}</td>
              <td v-if="taker.can_edit" class="column-action">
                <div class="row justify-content-center">
                  <div class="mx-2">
                    <donate-info :taker-id="taker.id" :is-edit="true" :edit-object="donate" />
                  </div>
                  <div class="me-2" v-if="taker.can_delete">
                    <i class="bi bi-x-circle fs-5 text-danger" :title="$t('common.delete')"
                      @click="handleDelete(donate.id)"></i>
                  </div>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <nav v-if="rows > page_size" class="mt-2 d-flex justify-content-center">
      <ul class="pagination">
        <li class="page-item" :class="{ disabled: page === 1 }">
          <a class="page-link" href="#" @click.prevent="page--">Previous</a>
        </li>
        <li class="page-item" v-for="n in Math.ceil(rows / page_size)" :key="n" :class="{ active: page === n }">
          <a class="page-link" href="#" @click.prevent="page = n">{{ n }}</a>
        </li>
        <li class="page-item" :class="{ disabled: page === Math.ceil(rows / page_size) }">
          <a class="page-link" href="#" @click.prevent="page++">Next</a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { userStoreObj } from '@/stores/users';
import { takersStoreObj } from '@/stores/takers';
import DonateInfo from "@/components/Main/DonateInfo.vue";
import { isMobile } from "@/helpers";

// Props definition in script setup syntax
const props = defineProps({
  takerId: {
    type: String,
    required: true
  }
});

const usersStore = userStoreObj();
const takersStore = takersStoreObj();

const page = ref(1);
const page_size = ref(0);
const showAddDonate = ref(false);

// Updated computed properties to use Pinia stores
const user = computed(() => usersStore.user);
const takers = computed(() => takersStore.takers);
const fetchingData = computed(() => takersStore.fetchingData);
const error = computed(() => takersStore.error);
const isWeb = computed(() => !isMobile());

const taker = computed(() => {
  let index = takers.value.findIndex((r) => r.id === props.takerId);
  return index >= 0 ? takers.value[index] : {};
});

const start = computed(() => (page.value - 1) * page_size.value);
const end = computed(() => page.value * page_size.value);
const rows = computed(() => taker.value.donates?.length || 0);

// Replace vue.$i18n with useI18n() composable
const { t } = useI18n();

// Updated methods to use Pinia store
const handleDelete = async (donateId) => {
  let res = confirm(t('common.confirmDelete'));
  if (res) {
    await takersStore.removeDonate(donateId);
  }
};

const initPaging = () => {
  page.value = 1;
  page_size.value = isWeb.value ? 15 : 7;
};

// Lifecycle hooks
onMounted(() => {
  initPaging();
});
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