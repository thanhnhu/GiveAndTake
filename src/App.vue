<template>
  <div id="app">
    <!--
    <h1>Django VueJs Template</h1>
    <div id="nav">
     <router-link :to="{ name: 'home' }">Vue</router-link> |
     <router-link :to="{ name: 'messages' }">Django Rest</router-link>
    </div>
    -->
    <app-header :user="user"></app-header>
    <router-view class="container-fluid"></router-view>
    <app-footer></app-footer>
  </div>
</template>

<script>
import { mapState } from "vuex";
import AppHeader from "@/components/AppHeader";
import AppFooter from "@/components/AppFooter";

export default {
  name: "app",
  components: { AppHeader, AppFooter },

  computed: {
    ...mapState({
      fetchingData: (state) => state.users.fetchingData,
      user: (state) => state.users.user,
      error: (state) => state.users.error,
    }),
  },
};
</script>

<style lang="scss" scoped>
#app {
  box-sizing: border-box;
  color: #37474f;
  font-family: "Lato", Helvetica, Arial, sans-serif;
  margin: 0 auto;
  padding: 0;
  text-align: center;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
}

.container-fluid {
  //height: 100vh;
  //min-height: calc(100vh - calc(100vh - 100%));
  padding-bottom: 4rem;
}
</style>