<template src="./donates.html"></template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';
import moment from 'moment';
import { userStoreObj } from '@/stores/users';
import { takersStoreObj } from '@/stores/takers';
import { isMobile } from "@/helpers";
import DonateInfo from "@/components/Main/DonateInfo.vue";

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

const { user } = storeToRefs(usersStore);
const { takers, fetchingData } = storeToRefs(takersStore);
const isWeb = computed(() => !isMobile());

const taker = computed(() => {
  let index = takers.value.findIndex((r) => r.id === props.takerId);
  return index >= 0 ? takers.value[index] : {};
});

const start = computed(() => (page.value - 1) * page_size.value);
const end = computed(() => page.value * page_size.value);
const rows = computed(() => taker.value.donates?.length || 0);

const { t } = useI18n();

const formatDate = (value) => {
  if (value) return moment(String(value)).format('YYYY/MM/DD HH:mm')
};

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
  if (!takersStore.takers.length) {
    takersStore.getTakers()
  }
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