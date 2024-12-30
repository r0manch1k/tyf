<template>
  <route-link
    :to="{ name: 'post-detail', params: { identifier: post.identifier } }"
  >
    <div class="card bg-dark mb-4 p-1">
      <div class="card-body fs-7">
        <div class="d-flex align-items-center justify-content-between">
          <h5 class="card-title fs-6">{{ post.title }}</h5>
          <div class="d-flex align-items-center gap-2">
            <router-link
              :to="{
                name: 'post-detail',
                params: { identifier: post.identifier },
              }"
              class="d-flex align-items-center gap-1 mb-2 fs-9"
            >
              <i class="bi bi-bookmark-fill"></i>
              <p class="m-0 p-0">{{ post.bookmarks }}</p>
            </router-link>
            <router-link
              :to="{
                name: 'post-detail',
                params: { identifier: post.identifier },
              }"
              class="d-flex align-items-center gap-1 mb-2 fs-9"
            >
              <i class="bi bi-chat-square-fill pt-0-5"></i>
              <p class="m-0 p-0">{{ post.comments }}</p>
            </router-link>
          </div>
        </div>

        <div class="card-text text-muted">
          {{ post.content }}
        </div>

        <div class="d-flex align-items-center justify-content-between">
          <div class="d-flex flex-grow-1 gap-2 align-items-center">
            <router-link
              :to="{
                name: 'profile',
                params: { username: post.author.username },
              }"
            >
              <img
                :src="post.author.avatar"
                alt="avatar"
                class="img-fluid rounded-circle"
                style="width: 30px; height: 30px"
              />
            </router-link>
            <div class="d-flex flex-column text-muted gap-0">
              <router-link
                :to="{
                  name: 'profile',
                  params: { username: post.author.username },
                }"
              >
                <p class="mb-0 link fs-9">
                  <strong>{{ post.author.username }}</strong>
                </p>
              </router-link>
              <p class="mb-0 fs-9">
                <strong>{{ post.created_at }}</strong>
              </p>
            </div>
          </div>

          <div class="d-flex align-items-center gap-1">
            <div class="me-1 fs-9">
              <router-link
                :to="{
                  name: 'post-detail',
                  params: { identifier: post.identifier },
                }"
                class="badge bg-secondary fs-9"
              >
                ...
              </router-link>
            </div>
            <router-link
              :to="{
                name: 'post-detail',
                params: { identifier: post.identifier },
              }"
              class="text-light"
            >
              <i class="bi bi-file fs-5 filetype"></i>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </route-link>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import type PostModel from "@/models/PostModel";

const props = defineProps({
  post: {
    type: Object as () => PostModel,
    required: true,
  },
});
</script>
