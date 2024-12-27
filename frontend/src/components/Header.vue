<template>
  <nav class="navbar navbar-expand bg-secondary px-4 py-1">
    <router-link :to="{ name: 'home' }" class="navbar-brand me-4">
      <img class="logo" src="@/assets/media/logo.svg" alt="tyf" />
    </router-link>

    <a
      data-bs-toggle="offcanvas"
      type="button"
      data-bs-target="#offcanvas"
      aria-controls="offcanvas"
    >
      <i class="bi bi-list fs-3 text-light"></i>
    </a>

    <div class="ms-4 w-100" id="search">
      <input
        id="search-input"
        class="form-control fs-6 bg-secondary-light border-0"
        type="search"
        placeholder="Search"
      />
    </div>

    <router-link :to="{ name: 'not-found' }" class="btn-0 fs-6 ms-4"
      >Create</router-link
    >

    <div class="navbar-nav align-items-center ms-0">
      <div class="nav-item dropdown ms-4" id="profile">
        <router-link
          :to="{ name: 'profile', params: { username: 'lazyRaisins9' } }"
          class="nav-link dropdown-toggle"
          data-bs-toggle="dropdown"
          id="profile-img-container"
        >
          <img
            class="rounded-circle"
            id="profile-img"
            :src="defaultAvatarUrl"
            v-if="!loading"
          />
        </router-link>

        <div
          class="dropdown-menu dropdown-menu-dark dropdown-menu-end bg-secondary border-0 rounded-0 rounded-bottom fs-6 mt-3"
        >
          <router-link
            :to="{ name: 'profile', params: { username: 'lazyRaisins9' } }"
            class="dropdown-item"
            >Profile</router-link
          >

          <router-link :to="{ name: 'login' }" class="dropdown-item"
            >Log In</router-link
          >

          <router-link :to="{ name: 'login' }" class="dropdown-item"
            >Log Out</router-link
          >
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";

const loading = ref(true);

const store = useStore();

// TODO: Hadle profile data

onMounted(async () => {
  await store.dispatch("profile/fetchStatic");
  loading.value = false;
});

const defaultAvatarUrl = computed(() => {
  return store.getters["profile/getDefaultAvatar"];
});
</script>

<style>
.logo {
  height: 35px;
}

#search-input {
  border-radius: 0.5em;
}

#search-input:focus {
  color: var(--light);
  background-color: var(--secondary-light);
  outline: var(--primary) solid 0.1em;
}

#profile {
  padding: 0;
  border: 0;
}

#profile-img-container {
  padding: 0;
}

#profile-img-container::after {
  display: none;
  border: 0;
  margin: 0;
  padding: 0;
}

#profile-img {
  width: 30px;
  height: 30px;
}
</style>
