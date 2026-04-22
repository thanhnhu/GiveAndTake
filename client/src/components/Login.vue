<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "login",
  data() {
    return {
      username: "",
      password: "",
      submitted: false,
      showAlert: 0,
    };
  },
  computed: {
    ...mapState("users", ["fetchingData", "user", "error"]),
  },
  methods: {
    ...mapActions("users", ["login"]),
    handleSubmit() {
      this.submitted = true;
      const { username, password } = this;
      if (username && password) {
        this.login({ username, password });
      }
    },
  },
  watch: {
    error() {
      if (this.error) {
        this.showAlert = 5;
      }
    },
  },
};
</script>

<template>
  <div>
    <h2>{{ $t('user.login') }}</h2>
    <b-alert :show="showAlert" @dismissed="showAlert = 0" variant="warning" dismissible fade>
      {{ $t('user.messages.wrong_username_password') }}
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
          <b-button type="submit" size="sm" variant="outline-primary" class="mr-2" :disabled="user || fetchingData">{{
            $t("user.login") }}</b-button>
          <b-button size="sm" variant="outline-secondary" to="/register">{{ $t("user.register") }}</b-button>
        </b-col>
      </b-form-row>
    </form>
  </div>
</template>

<style lang="scss" scoped></style>