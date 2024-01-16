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
    <h2>Đăng nhập</h2>
    <b-alert
      :show="showAlert"
      @dismissed="showAlert = 0"
      variant="warning"
      dismissible
      fade
    >
      Tên đăng nhập hoặc mật khẩu không đúng!
    </b-alert>
    <form @submit.prevent="handleSubmit">
      <b-form-row class="mb-2">
        <b-col>
          <input
            type="text"
            v-model="username"
            name="username"
            class="form-control"
            placeholder="Tên đăng nhập"
            :class="{ 'is-invalid': submitted && !username }"
          />
          <div v-show="submitted && !username" class="error-messages">
            Tên đăng nhập không để trống!
          </div>
        </b-col>
      </b-form-row>

      <b-form-row class="mb-4">
        <b-col>
          <input
            type="password"
            v-model="password"
            name="password"
            class="form-control"
            placeholder="Mật khẩu"
            :class="{ 'is-invalid': submitted && !password }"
          />
          <div v-show="submitted && !password" class="error-messages">
            Mật khẩu không để trống!
          </div>
        </b-col>
      </b-form-row>

      <b-form-row>
        <b-col>
          <b-button
            type="submit"
            size="sm"
            variant="outline-primary"
            class="mr-2"
            :disabled="user || fetchingData"
            >{{ $t("user.login") }}</b-button
          >
          <b-button size="sm" variant="outline-secondary" to="/register"
            >{{ $t("user.register") }}</b-button
          >
        </b-col>
      </b-form-row>
    </form>
  </div>
</template>

<style lang="scss" scoped>
</style>