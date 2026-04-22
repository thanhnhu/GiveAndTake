<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "app-header",

  props: {
    user: Object,
  },

  data: () => ({
    optionLangs: {
      'en': 'English',
      'vi': 'Tiếng Việt'
    }
  }),

  computed: {
    ...mapGetters("langs", ["getLang"]),
    langsFiltered() {
      return Object.keys(this.optionLangs)
        .filter(key => key !== this.getLang)
        .reduce((obj, key) => {
          obj[key] = this.optionLangs[key];
          return obj;
        }, {});
    }
  },

  methods: {
    ...mapActions("langs", ["setLang"]),
    ...mapActions("users", ["logout"]),
    callSetLangActions(event) {
      this.setLang(event.target.getAttribute('value'));
    }
  },
};
</script>

<template>
  <div class="mb-2">
    <b-navbar toggleable="sm" type="light" variant="info">
      <b-navbar-brand href="#">
        <img src="/static/fire.png" />
        <em>{{ $t('common.giveandforget') }}</em>
      </b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav fill>
          <b-nav-item to="/">{{ $t('common.taker') }}</b-nav-item>
          <b-nav-item to="/givers">{{ $t('common.giver') }}</b-nav-item>
          <b-nav-item to="/intro">{{ $t('common.introduce') }}</b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">

          <b-nav-item-dropdown :text="optionLangs[getLang]" right>
            <b-dropdown-item v-for="(value, key) in langsFiltered" :key="key" :value="key"
              @click.prevent="callSetLangActions">{{ value }}</b-dropdown-item>
            <div v-if="user" class="mx-2">
              <em>{{ $t('user.hello') }}, {{ user.username }}</em>
              <b-dropdown-item @click="logout">{{ $t('user.logout') }}</b-dropdown-item>
            </div>
            <div v-else class="mx-2">
              <b-nav-item to="/login">{{ $t('user.login') }}</b-nav-item>
              <b-nav-item to="/register">{{ $t('user.register') }}</b-nav-item>
            </div>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<style lang="scss" scoped>
.navbar {
  padding: 0 0.5rem;
}

.navbar-brand {
  padding-top: 0.5rem;

  img {
    padding-bottom: 0.5rem;
  }
}
</style>
