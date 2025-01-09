<template>
  <div class="d-flex align-items-center gap-2 text-start">
    <router-link
      :to="{
        name: 'profile',
        params: { username: profile.username },
      }"
    >
      <img
        :src="profile.avatar"
        alt="avatar"
        class="img-fluid rounded-circle"
        style="width: 40px; height: 40px"
      />
    </router-link>
    <div class="d-flex flex-column">
      <router-link
        :to="{
          name: 'profile',
          params: { username: profile.username },
        }"
        class="link-primary fw-bold fst-italic fs-6"
        style="height: 20px"
      >
        {{ profile.username }}
      </router-link>
      <router-link
        :to="{
          name: 'profile',
          params: { username: profile.username },
        }"
        class="btn-secondary-x-light fs-7"
      >
        {{ created_at }}
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

const created_at = moment(props.profile.date_joined).fromNow();
</script>
