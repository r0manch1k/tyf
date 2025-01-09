<template>
  <nav class="header navbar navbar-expand bg-dark-light fixed-top px-4 py-1">
    <router-link :to="{ name: 'home' }" class="header__logo navbar-brand me-4">
      <img class="logo" src="@/assets/media/logo.svg" alt="tyf" />
    </router-link>

    <a
      class="header__sidebar-button"
      data-bs-toggle="offcanvas"
      type="button"
      data-bs-target="#offcanvas"
      aria-controls="offcanvas"
    >
      <i class="bi bi-list fs-4 text-light"></i>
    </a>

    <div class="header__search ms-4 w-100">
      <input
        class="header__search-input form-control fs-6 bg-dark-light border-0"
        type="search"
        placeholder="Поиск"
      />
    </div>

    <router-link
      :to="{ name: 'home' }"
      class="header__create-button btn-light fs-6 ms-4"
      v-if="profile"
      >Добавить пост</router-link
    >

    <!-- <router-link
      :to="{ name: 'home' }"
      class="header__notifications-button btn-light fs-6 ms-4"
      >Notifications(10)</router-link
    > -->

    <a
      href="notifications"
      class="header__notifications-button btn-light fs-5 ms-4"
      v-if="profile"
      ><i class="bi bi-bell"></i
    ></a>

    <div class="header__dropdown-container navbar-nav align-items-center ms-0">
      <div class="header__profile-container nav-item dropdown ms-4">
        <router-link
          :to="{ name: 'profile', params: { username: 'somberCod0' } }"
          class="header__profile-img-container nav-link dropdown-toggle"
          data-bs-toggle="dropdown"
        >
          <img
            class="header__profile-img rounded-circle"
            :src="profile.avatar"
            v-if="!loading && profile"
          />
          <a v-else class="header__profile-img btn-light fs-6">Вход</a>
        </router-link>

        <div
          class="header__dropdown dropdown-menu dropdown-menu-dark dropdown-menu-end bg-secondary border-0 rounded-0 rounded-bottom fs-6"
        >
          <router-link
            :to="{ name: 'profile', params: { username: 'somberCod0' } }"
            class="header__profile-button dropdown-item"
            >Профиль</router-link
          >

          <router-link
            :to="{ name: 'login' }"
            class="header__login-button dropdown-item"
            >Вход</router-link
          >

          <!-- <router-link :to="{ name: 'login' }" class="header__logout-button dropdown-item"
            ><i class="bi bi-box-arrow-in-left"></i> Log Out</router-link
          > -->
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
// import { useStore } from "vuex";

const loading = ref(true);

// const store = useStore();

// TODO: Hadle profile data

onMounted(() => {
  loading.value = false;
});

const profile = computed(() => {
  return null;
});
</script>

<style>
.logo {
  height: 30px;
}

/* TODO: Suka u menya gorit chto nelza oveeride bootstrap styles, ya prosto viebal !important */

.header__search-input {
  border-radius: 0.4em !important;
}

.header__search-input:focus {
  color: var(--light) !important;
  background-color: var(--dark-light) !important;
  outline: var(--primary) solid 0.1em !important;
}

input[type="search"]::-webkit-search-cancel-button {
  -webkit-appearance: none;
  appearance: none;
}

.header__profile-container {
  padding: 0 !important;
  border: 0 !important;
}

.header__profile-img-container {
  padding: 0 !important;
}

.header__profile-img-container::after {
  display: none !important;
  border: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
}

.header__profile-img {
  width: 30px !important;
  height: 30px !important;
}

.header__create-button {
  white-space: nowrap;
}
</style>
