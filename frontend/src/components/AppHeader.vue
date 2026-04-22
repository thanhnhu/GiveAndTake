<template>
  <div class="mb-2">
    <BNavbar toggleable="sm" type="light" variant="info">
      <BNavbarBrand href="#">
        <img src="@/assets/fire.png" />
        <em>{{ $t('common.giveandforget') }}</em>
      </BNavbarBrand>
      <BNavbarToggle target="nav-collapse"></BNavbarToggle>
      <BCollapse id="nav-collapse" isNav>
        <BNavbarNav fill>
          <BNavItem to="/">{{ $t('common.taker') }}</BNavItem>
          <BNavItem to="/givers">{{ $t('common.giver') }}</BNavItem>
          <BNavItem to="/intro">{{ $t('common.introduce') }}</BNavItem>
        </BNavbarNav>

        <BNavbarNav class="ms-auto mb-2 mb-lg-0">
          <BNavItemDropdown :text="optionLangs[getLang]" right>
            <BDropdownItem v-for="(value, key) in langsFiltered" :key="key" @click.prevent="setLang(key)">
              {{ value }}
            </BDropdownItem>
          </BNavItemDropdown>
          <BNavItemDropdown right v-if="user">
            <template #button-content>
              <em>{{ $t('user.hello') }}, {{ user.username }}</em>
            </template>
            <BDropdownItem @click="logout">{{ $t('user.logout') }}</BDropdownItem>
          </BNavItemDropdown>
          <BNavItemDropdown right v-else>
            <template #button-content>
              <em>{{ $t('user.hello') }}</em>
            </template>
            <BNavItem to="/login">{{ $t('user.login') }}</BNavItem>
            <BNavItem to="/register">{{ $t('user.register') }}</BNavItem>
          </BNavItemDropdown>
        </BNavbarNav>
      </BCollapse>
    </BNavbar>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { userStoreObj } from '@/stores/users'
import { langStoreObj } from '@/stores/langs'

const optionLangs = ref({
  'en': 'English',
  'vi': 'Tiếng Việt'
})

const userStore = userStoreObj()
const langStore = langStoreObj()

// Use storeToRefs for reactive store properties
const { user } = storeToRefs(userStore)
const { getLang } = storeToRefs(langStore)

const langsFiltered = computed(() => {
  return Object.keys(optionLangs.value)
    .filter(key => key !== getLang.value)
    .reduce((obj, key) => {
      obj[key] = optionLangs.value[key]
      return obj
    }, {})
})

// Methods
const setLang = (lang) => {
  langStore.setLang(lang)
}

const logout = () => {
  userStore.logout()
}
</script>

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
