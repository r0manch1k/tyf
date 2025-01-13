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
        class="profile-list-item__username fs-6 fw-bold"
      >
        {{ profile.username }}
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, inject } from "vue";
import type ProfileListItem from "@/models/ProfileModel";

const moment = inject("moment") as any;

const props = defineProps<{
  profile: ProfileListItem;
}>();
</script>

<style scoped>
.profile-list-item {
  width: fit-content;
}
</style>
