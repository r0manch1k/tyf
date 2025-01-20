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
import type ProfileListItem from "@/models/ProfileModel";
import { defineProps, inject } from "vue";

const moment = inject("moment");

const props = defineProps<{
  profile: ProfileListItem;
}>();

// @ts-expect-error: Unreachable code error
moment(props.profile.date_joined).fromNow();
// const created_at = moment(props.profile.date_joined).fromNow();
</script>

<style scoped>
.profile-list-item {
  width: fit-content;
}
</style>
