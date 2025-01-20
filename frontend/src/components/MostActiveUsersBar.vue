<template>
  <div class="most-active-users-bar bg-dark-light p-1">
    <div class="most-active-users-bar__list" v-if="!loading">
      <h3
        class="most-active-users-bar__title fs-6 text-light p-1 m-0 text-start text-decoration-none"
      >
        <span class="text-decoration-underline">Топ 5</span>
        <span class="most-active-users-bar__emoji"> 🤓</span>
      </h3>
      <h4
        class="most-active-users-bar__subtitle fs-6 text-secondary-xx-light p-1 m-0 fw-normal text-start"
      >
        Пользователи с наибольшим количеством постов за все время
      </h4>
      <table
        class="most-active-users-bar__table table table--dark-light table--striped"
      >
        <thead class="most-active-users-bar__thead">
          <tr class="most-active-users-bar__tr">
            <th
              scope="col"
              class="most-active-users-bar__th text-start fw-normal"
            >
              Пользователь
            </th>
            <th scope="col" class="most-active-users-bar__th fw-normal">
              Посты
            </th>
          </tr>
        </thead>
        <tbody class="most-active-users-bar__tbody">
          <tr
            v-for="user in users"
            :key="user.username"
            class="most-active-users-bar__tr"
          >
            <td class="most-active-users-bar__td align-middle text-center">
              <ProfileListItem :profile="user" />
            </td>
            <td class="most-active-users-bar__td align-middle">
              <router-link
                :to="{ name: 'profile', params: { username: user.username } }"
                class="most-active-users-bar__link btn-light fs-7 text-decoration-none"
              >
                {{ user.posts_count }}
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <LoadingCircle
      v-else
      class="most-active-users-bar__loading-circle spinner-border-sm"
    />
  </div>
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

<style scoped>
.table {
  margin: 0;
}

.table > :not(caption) > * > * {
  border-top-width: 0;
  border-bottom-width: 0;
  padding: 0.2rem 0.4rem;
}

.most-active-users-bar {
  border-radius: 0.4rem;
  /* border: 1px solid var(--secondary); */
}
</style>
