<template>
  <div class="most-active-users-bar bg-dark-light p-2" v-if="!loading">
    <div class="most-active-users-bar__list">
      <table
        class="most-active-users-bar__table table table-dark-light table-striped"
      >
        <thead>
          <tr>
            <th scope="col">Пользователь</th>
            <th scope="col">Посты</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.username">
            <td class="align-middle text-center">
              <ProfileListItem :profile="user" />
            </td>
            <td class="align-middle">
              <router-link
                :to="{ name: 'profile', params: { username: user.username } }"
                class="btn-light fs-7"
              >
                {{ user.posts_count }}
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <LoadingCircle v-else />
</template>

<script setup lang="ts">
import LoadingCircle from "@/components/LoadingCircle.vue";
import ProfileListItem from "@/components/ProfileListItem.vue";
import type ProfileListItemModel from "@/models/ProfileModel";
import ProfileDataService from "@/services/ProfileDataService";
import { onMounted, ref } from "vue";

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
}
</style>
