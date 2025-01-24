<template>
  <div class="profile-list-item d-flex align-items-center gap-2">
    <router-link
      :to="{
        name: 'profile',
        params: { username: profile.username },
      }"
      class="profile-list-item__avatar-link"
    >
      <img
        :src="profile.avatar"
        alt="avatar"
        class="profile-list-item__avatar img-fluid rounded-circle"
        style="width: 35px; height: 35px"
      />
    </router-link>
    <div class="profile-list-item__details d-flex flex-column">
      <router-link
        :to="{
          name: 'profile',
          params: { username: profile.username },
        }"
        class="profile-list-item__username fs-6 text-start"
      >
        <span v-if="profile.username.length > 17">
          {{ profile.username.substring(0, 17) + "..." }}
        </span>
        <span v-else>
          {{ profile.username }}
        </span>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ProfileListItemModel } from "@/models/ProfileModel";
import { defineProps } from "vue";

const props = defineProps<{
  profile: ProfileListItemModel;
}>();
</script>

<style scoped>
.profile-list-item {
  width: fit-content;
}

.profile-list-item__username:hover {
  color: var(--primary);
}
</style>
