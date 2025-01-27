<template>
  <nav class="header navbar navbar-expand bg-dark-light fixed-top px-4 py-1">
    <router-link :to="{ name: 'home' }" class="header__logo navbar-brand mx-auto">
      <img class="logo" src="@/assets/media/logo.svg" alt="tyf" />
    </router-link>

    <!-- <a
      class="header__sidebar-button"
      type="button"
      data-bs-toggle="offcanvas"
      data-bs-target="#offcanvas"
      aria-controls="offcanvas"
    >
      <i class="bi bi-list fs-4 text-light"></i>
    </a> -->

    <div class="header__search ms-4 w-100">
      <SearchBar v-if="isHome" />
    </div>

    <router-link
      :to="{ name: 'post-create' }"
      class="header__create-button btn-light fs-6 ms-4"
      v-if="isAuth && !loading"
      >Создать</router-link
    >

    <!-- <router-link
      :to="{ name: 'chats' }"
      class="header__messages-button btn-light fs-6 ms-4"
      v-if="isAuth && !loading"
      >Чаты</router-link
    > -->

    <router-link
      :to="{ name: 'notifications' }"
      class="header__notifications-button btn-light fs-6 ms-4"
      v-if="isAuth && !loading"
      >Уведомления({{ notificationsUnread.length }})</router-link
    >

    <div class="header__dropdown-container navbar-nav align-items-center ms-0">
      <div class="header__profile-container nav-item dropdown ms-4">
        <a
          v-if="isAuth && !loading"
          class="header__profile-img-container nav-link dropdown-toggle"
          data-bs-toggle="dropdown"
        >
          <img
            class="header__profile-img rounded-circle"
            :src="profile.avatar"
          />
        </a>

        <LoadingCircle
          v-if="loading"
          class="spinner-border-sm mx-auto my-auto"
        />

        <router-link
          v-if="!isAuth && !loading"
          class="header__profile-img btn-light fs-6"
          :to="{ name: 'login' }"
          >Вход</router-link
        >

        <div
          class="header__dropdown dropdown-menu dropdown-menu-dark dropdown-menu-end bg-secondary border-0 rounded fs-6 mt-3"
        >
          <router-link
            v-if="isAuth"
            :to="{ name: 'profile', params: { username: profile.username } }"
            class="header__profile-button dropdown-item"
            >Профиль</router-link
          >

          <router-link
            v-if="!isAuth"
            :to="{ name: 'login' }"
            class="header__login-button dropdown-item"
            >Вход</router-link
          >

          <router-link
            v-if="isAuth"
            :to="{ name: 'logout' }"
            class="header__login-button dropdown-item"
            >Выйти</router-link
          >
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import LoadingCircle from "@/components/LoadingCircle.vue";
import SearchBar from "@/components/SearchBar.vue";
import type NotificationModel from "@/models/NotificationModel";
import type ProfileListItemModel from "@/models/ProfileModel";
import { computed } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

const store = useStore();
const route = useRoute();

const loading = computed(() => store.state.profile.loading);
const profile = computed<ProfileListItemModel>(
  () => store.state.profile.profile
);

const notifications = computed<NotificationModel[]>(
  () => store.state.notification.notifications
);
const notificationsUnread = computed<NotificationModel[]>(() => {
  if (notifications.value.length === 0) return [];
  return notifications.value.filter((notification) => !notification.read);
});

const isAuth = computed(() => profile.value.id > -1);
const isHome = computed(() => route.path === "/");
</script>

<style>
.logo {
  height: 30px;
}

/* TODO: Suka u menya gorit chto nelza oveeride bootstrap styles, ya prosto viebal !important */

/* .header {
  border-bottom: 1px solid var(--secondary) !important;
} */

.dropdown-menu-dark .dropdown-item.active,
.dropdown-menu-dark .dropdown-item:active {
  background-color: var(--secondary) !important;
  color: var(--light) !important;
}

.dropdown-menu-dark .dropdown-item:hover,
.dropdown-menu-dark .dropdown-item:focus {
  color: var(--light) !important;
}

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
