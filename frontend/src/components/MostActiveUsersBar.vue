<template>
  <div class="most-active-users card bg-dark-light" v-if="!loading">
    <div class="most-active-users__header card-header py-2 text-start">
      <h2
        class="most-active-users__title card-title fs-6 text-light text-decoration-underline m-0"
      >
        Топ 5
      </h2>
      <!-- <h3
        class="most-active-users__description fs-7 text-secondary-x-light fw-normal"
      >
        Пользователи с наибольшим количеством публикаций
      </h3> -->
    </div>
    <div class="most-active-users__list card-body">
      <div
        v-for="user in users"
        :key="user.username"
        class="most-active-users__user"
      >
        <div class="d-flex align-items-center justify-content-between">
          <ProfileListItem :profile="user" />
          <router-link
            :to="{ name: 'profile', params: { username: user.username } }"
            class="btn-secondary-x-light fs-7"
          >
            Постов: {{ user.posts_count }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
  <LoadingCircle v-else />
</template>

<script setup lang="ts">
import LoadingCircle from "@/components/LoadingCircle.vue";
import ProfileListItem from "@/components/ProfileListItem.vue";
import ProfileDataService from "@/services/ProfileDataService";
import type ProfileListItemModel from "@/models/ProfileModel";
import { ref, onMounted } from "vue";

const loading = ref(true);

const users = ref<ProfileListItemModel[]>([]);

onMounted(async () => {
  users.value = await ProfileDataService.getMostActiveProfiles();
  loading.value = false;
});
</script>

<style scoped></style>
