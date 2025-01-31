<template>
  <div id="app">
    <app-header :user="user"></app-header>
    <router-view class="container-fluid"></router-view>
    <app-footer></app-footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { userStoreObj } from '@/stores/users'
import AppHeader from "@/components/AppHeader.vue"
import AppFooter from "@/components/AppFooter.vue"

const { user, fetchingData, error } = storeToRefs(userStoreObj)

onMounted(() => {
  console.log('App mounted')
  console.log('Current user:', user?.value)
  console.log('Current route:', window.location.pathname)
})
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