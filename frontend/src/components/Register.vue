<script setup>
import { ref } from 'vue';
import { storeToRefs } from 'pinia';
import { Form, Field } from 'vee-validate';
import { userStoreObj } from '@/stores/users';

const userStore = userStoreObj();

const user = ref({
  username: "",
  password: "",
  email: "",
  first_name: "",
  last_name: "",
});
const showAlert = ref(0);

const { fetchingData, error } = storeToRefs(userStore);

// Methods
const onSubmit = async () => {
  await userStore.register(user.value);
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
    <Form @submit="onSubmit">
      <b-overlay :show="fetchingData" variant="transparent">
        <b-form-row class="mb-2">
          <b-col>
            <Field :name="$t('user.input_text.username')" rules="required" v-slot="{ field, errors }">
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.length > 0 }"
                :placeholder="$t('user.input_text.username')" v-model="user.username" v-bind="field" />
              <div class="error-messages">{{ errors[0] }}</div>
            </Field>
          </b-col>
        </b-form-row>

        <b-form-row class="mb-2">
          <b-col>
            <Field :name="$t('user.input_text.password')" rules="required" v-slot="{ field, errors }">
              <input type="password" class="form-control" :class="{ 'is-invalid': errors.length > 0 }"
                :placeholder="$t('user.input_text.password')" v-model="user.password" v-bind="field" />
              <div class="error-messages">{{ errors[0] }}</div>
            </Field>
          </b-col>
        </b-form-row>

        <b-form-row class="mb-2">
          <b-col>
            <Field :name="$t('user.input_text.email')" rules="required|email" v-slot="{ field, errors }">
              <input type="email" v-model="user.email" class="form-control" placeholder="Email"
                :class="{ 'is-invalid': errors.length > 0 }" v-bind="field" />
              <div class="error-messages">{{ errors[0] }}</div>
            </Field>
          </b-col>
        </b-form-row>

        <b-form-row class="mb-2">
          <b-col>
            <Field :name="$t('user.input_text.firstname')" rules="required" v-slot="{ field, errors }">
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.length > 0 }"
                :placeholder="$t('user.input_text.firstname')" v-model="user.first_name" v-bind="field" />
              <div class="error-messages">{{ errors[0] }}</div>
            </Field>
          </b-col>
        </b-form-row>

        <b-form-row class="mb-4">
          <b-col>
            <Field :name="$t('user.input_text.lastname')" rules="required" v-slot="{ field, errors }">
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.length > 0 }"
                :placeholder="$t('user.input_text.lastname')" v-model="user.last_name" v-bind="field" />
              <div class="error-messages">{{ errors[0] }}</div>
            </Field>
          </b-col>
        </b-form-row>

        <b-form-row>
          <b-col>
            <b-button type="submit" size="sm" variant="outline-primary" class="me-2" :disabled="fetchingData">{{
              $t("user.register") }}</b-button>
            <b-button size="sm" variant="outline-secondary" to="/login">{{ $t("common.cancel") }}</b-button>
          </b-col>
        </b-form-row>
      </b-overlay>
    </Form>
  </div>
</template>

<style lang="scss" scoped></style>