<template>
  <div class="profile-list-item-large p-3 pb-0">
    <router-link
      :to="{ name: 'profile', params: { username: profile.username } }"
      class="profile-list-item-large__link"
    >
      <div class="profile-list-item-large__avatar-container mb-3">
        <img
          class="profile-list-item-large__avatar img-fluid rounded-circle"
          :src="profile.avatar"
          alt="Аватар пользователя"
          style="width: 12rem; height: 12rem"
        />
      </div>
      <div class="profile-list-item-large__content">
        <h3 class="profile-list-item-large__username fs-5 m-0">
          {{ profile.username }}
        </h3>
        <p class="profile-list-item-large__bio">{{ profile.bio }}</p>
      </div>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import type ProfileListItem from "@/models/ProfileModel";

const props = defineProps<{
  profile: ProfileListItem;
}>();
</script>

<style scoped>
/* .profile-list-item-large:hover {
  border-radius: 0.4rem;
  background-color: rgba(50, 50, 50, 0.2);
} */

/* .profile-list-item-large:hover .profile-list-item-large__avatar {
  box-shadow: 0 0 1rem rgba(50, 50, 50, 0.8);
  border-radius: 50%;
} */
</style>
