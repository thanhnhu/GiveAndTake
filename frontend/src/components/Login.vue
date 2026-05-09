<script setup>
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { storeToRefs } from 'pinia';
import { userStoreObj } from '@/stores/users';
import { translateError } from '@/helpers';

const { t, te } = useI18n();
const userStore = userStoreObj();
const username = ref("");
const password = ref("");
const submitted = ref(false);

const { fetchingData, user, error } = storeToRefs(userStore);

// Methods
const handleSubmit = async () => {
  submitted.value = true;
  if (username.value && password.value) {
    await userStore.login({
      username: username.value,
      password: password.value
    });
  }
};
</script>

<template>
  <div>
    <h2>{{ $t('user.login') }}</h2>
    <b-alert :show="!!error" variant="warning" dismissible @dismissed="userStore.error = null">
      {{ translateError(error, t, te) || $t('user.messages.wrong_username_password') }}
    </b-alert>
    <form @submit.prevent="handleSubmit">
      <b-form-row class="mb-2">
        <b-col>
          <input type="text" class="form-control" :class="{ 'is-invalid': submitted && !username }"
            :placeholder="$t('user.input_text.username')" name="username" v-model="username" />
          <div v-show="submitted && !username" class="error-messages">
            {{ $t('user.messages.username_required') }}</div>
        </b-col>
      </b-form-row>

      <b-form-row class="mb-4">
        <b-col>
          <input type="password" class="form-control" :class="{ 'is-invalid': submitted && !password }"
            :placeholder="$t('user.input_text.password')" name="password" v-model="password" />
          <div v-show="submitted && !password" class="error-messages">
            {{ $t('user.messages.password_required') }}</div>
        </b-col>
      </b-form-row>

      <b-form-row>
        <b-col>
          <b-button type="submit" size="sm" variant="outline-primary" class="me-2" :disabled="user || fetchingData">{{
            $t("user.login") }}</b-button>
          <b-button size="sm" variant="outline-secondary" to="/register">{{ $t("user.register") }}</b-button>
        </b-col>
      </b-form-row>
    </form>
  </div>
</template>

<style lang="scss" scoped></style>