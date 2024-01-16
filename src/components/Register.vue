<script>
import { mapState, mapActions } from "vuex";

export default {
  data() {
    return {
      user: {
        username: "",
        password: "",
        email: "",
        first_name: "",
        last_name: "",
      },
      showAlert: 0,
    };
  },
  computed: {
    ...mapState("users", ["fetchingData", "error"]),
  },
  methods: {
    ...mapActions("users", ["register"]),
    onSubmit() {
      this.register(this.user);
    },

    onOverlayHidden() {
      if (this.error) {
        this.showAlert = 5;
      }
    },
  },
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
        <b-overlay
          :show="fetchingData"
          variant="transparent"
          @hidden="onOverlayHidden"
        >
          <b-form-row class="mb-2">
            <b-col>
              <ValidationProvider
                name="Tên tài khoản"
                rules="required"
                v-slot="{ errors }"
              >
                <input
                  type="text"
                  v-model="user.username"
                  class="form-control"
                  placeholder="Tên tài khoản"
                  :class="{ 'is-invalid': errors.length > 0 }"
                />
                <div class="error-messages">{{ errors[0] }}</div>
              </ValidationProvider>
            </b-col>
          </b-form-row>

          <b-form-row class="mb-2">
            <b-col>
              <ValidationProvider
                name="Mật khẩu"
                rules="required"
                v-slot="{ errors }"
              >
                <input
                  type="password"
                  v-model="user.password"
                  class="form-control"
                  placeholder="Mật khẩu"
                  :class="{ 'is-invalid': errors.length > 0 }"
                />
                <div class="error-messages">{{ errors[0] }}</div>
              </ValidationProvider>
            </b-col>
          </b-form-row>

          <b-form-row class="mb-2">
            <b-col>
              <ValidationProvider
                name="Email"
                rules="required|email"
                v-slot="{ errors }"
              >
                <input
                  type="email"
                  v-model="user.email"
                  class="form-control"
                  placeholder="Email"
                  :class="{ 'is-invalid': errors.length > 0 }"
                />
                <div class="error-messages">{{ errors[0] }}</div>
              </ValidationProvider>
            </b-col>
          </b-form-row>

          <b-form-row class="mb-2">
            <b-col>
              <ValidationProvider
                name="Họ"
                rules="required"
                v-slot="{ errors }"
              >
                <input
                  type="text"
                  v-model="user.first_name"
                  class="form-control"
                  placeholder="Họ"
                  :class="{ 'is-invalid': errors.length > 0 }"
                />
                <div class="error-messages">{{ errors[0] }}</div>
              </ValidationProvider>
            </b-col>
          </b-form-row>

          <b-form-row class="mb-4">
            <b-col>
              <ValidationProvider
                name="Tên"
                rules="required"
                v-slot="{ errors }"
              >
                <input
                  type="text"
                  v-model="user.last_name"
                  class="form-control"
                  placeholder="Tên"
                  :class="{ 'is-invalid': errors.length > 0 }"
                />
                <div class="error-messages">{{ errors[0] }}</div>
              </ValidationProvider>
            </b-col>
          </b-form-row>

          <b-form-row>
            <b-col>
              <b-button
                type="submit"
                size="sm"
                variant="outline-primary"
                class="mr-2"
                :disabled="fetchingData"
                >{{ $t("user.register") }}</b-button
              >
              <b-button size="sm" variant="outline-secondary" to="/login"
                >{{ $t("common.cancel") }}</b-button
              >
            </b-col>
          </b-form-row>
        </b-overlay>
      </form>
    </ValidationObserver>
  </div>
</template>

<style lang="scss" scoped>
</style>