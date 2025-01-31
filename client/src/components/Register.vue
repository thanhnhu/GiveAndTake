<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { userStoreObj } from '@/stores/users';

const userStore = userStoreObj();
const router = useRouter();

const user = ref({
  username: "",
  password: "", 
  email: "",
  first_name: "",
  last_name: "",
});
const showAlert = ref(0);

// Computed properties
const fetchingData = computed(() => userStore.loading);
const error = computed(() => userStore.error);

// Methods
const onSubmit = async () => {
  await userStore.register(user.value);
};

const onOverlayHidden = () => {
  if (error.value) {
    showAlert.value = 5;
  }
};
</script>

<template>
  <div>
    <h2>{{ $t("user.register") }}</h2>
    <b-alert variant="warning" dismissible fade :show="showAlert" @dismissed="showAlert = 0">
      {{ $t("user.userExist") }}
    </b-alert>
    <ValidationObserver v-slot="{ handleSubmit }">
      <form @submit.prevent="handleSubmit(onSubmit)">
        <b-overlay :show="fetchingData" variant="transparent" @hidden="onOverlayHidden">
          <b-form-row class="mb-2">
            <b-col>
              <ValidationProvider :name="$t('user.input_text.username')" rules="required" v-slot="{ errors }">
                <input type="text" class="form-control" :class="{ 'is-invalid': errors.length > 0 }"
                  :placeholder="$t('user.input_text.username')" v-model="user.username" />
                <div class="error-messages">{{ errors[0] }}</div>
              </ValidationProvider>
            </b-col>
          </b-form-row>

          <b-form-row class="mb-2">
            <b-col>
              <ValidationProvider :name="$t('user.input_text.password')" rules="required" v-slot="{ errors }">
                <input type="password" class="form-control" :class="{ 'is-invalid': errors.length > 0 }"
                  :placeholder="$t('user.input_text.password')" v-model="user.password" />
                <div class="error-messages">{{ errors[0] }}</div>
              </ValidationProvider>
            </b-col>
          </b-form-row>

          <b-form-row class="mb-2">
            <b-col>
              <ValidationProvider :name="$t('user.input_text.email')" rules="required|email" v-slot="{ errors }">
                <input type="email" v-model="user.email" class="form-control" placeholder="Email"
                  :class="{ 'is-invalid': errors.length > 0 }" />
                <div class="error-messages">{{ errors[0] }}</div>
              </ValidationProvider>
            </b-col>
          </b-form-row>

          <b-form-row class="mb-2">
            <b-col>
              <ValidationProvider :name="$t('user.input_text.firstname')" rules="required" v-slot="{ errors }">
                <input type="text" class="form-control" :class="{ 'is-invalid': errors.length > 0 }"
                  :placeholder="$t('user.input_text.firstname')" v-model="user.first_name" />
                <div class="error-messages">{{ errors[0] }}</div>
              </ValidationProvider>
            </b-col>
          </b-form-row>

          <b-form-row class="mb-4">
            <b-col>
              <ValidationProvider :name="$t('user.input_text.lastname')" rules="required" v-slot="{ errors }">
                <input type="text" class="form-control" :class="{ 'is-invalid': errors.length > 0 }"
                  :placeholder="$t('user.input_text.lastname')" v-model="user.last_name" />
                <div class="error-messages">{{ errors[0] }}</div>
              </ValidationProvider>
            </b-col>
          </b-form-row>

          <b-form-row>
            <b-col>
              <b-button type="submit" size="sm" variant="outline-primary" class="mr-2" :disabled="fetchingData">{{
                $t("user.register") }}</b-button>
              <b-button size="sm" variant="outline-secondary" to="/login">{{ $t("common.cancel") }}</b-button>
            </b-col>
          </b-form-row>
        </b-overlay>
      </form>
    </ValidationObserver>
  </div>
</template>

<style lang="scss" scoped></style>