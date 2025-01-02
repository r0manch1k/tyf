<template>
  <div class="card text-start bg-secondary mb-3">
    <div
      class="card-header d-flex flex-row align-items-center justify-content-between"
    >
      <div class="d-flex align-items-center gap-2">
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
            style="width: 40px; height: 40px"
          />
        </router-link>
        <div class="d-flex flex-column align-items-center gap-0">
          <router-link
            :to="{
              name: 'profile',
              params: { username: post.author.username },
            }"
            class="btn-1 fs-6"
          >
            {{ post.author.username }}
          </router-link>
          <router-link
            :to="{
              name: 'post-detail',
              params: { identifier: post.identifier },
            }"
            class="text-secondary-x-light fs-6"
          >
            <time :datetime="post.created_at">{{ created_at }}</time>
          </router-link>
        </div>
      </div>
      <div class="d-flex flex-row gap-2" v-if="post.tags">
        <Tag v-for="tag in post.tags" :key="tag.id" :tag="tag" />
      </div>
    </div>

    <div class="card-body">
      <router-link
        :to="{
          name: 'post-detail',
          params: { identifier: post.identifier },
        }"
      >
        <h5 class="card-title text-light">{{ post.title }}</h5>
      </router-link>
      <img
        v-if="post.thumbnail"
        :src="post.thumbnail"
        class="card-img-top my-3"
        alt="post-thumbnail"
      />
      <p class="card-text text-light">{{ post.description }}</p>
      <router-link
        :to="{
          name: 'post-detail',
          params: { identifier: post.identifier },
        }"
        class="btn btn-primary"
      >
        Читать полностью
      </router-link>
    </div>
    <div
      class="card-footer d-flex flex-row align-items-center justify-content-between"
    >
      <div class="d-flex align-items-center gap-4">
        <router-link
          :to="{
            name: 'post-detail',
            params: { identifier: post.identifier },
          }"
          class="d-flex align-items-center gap-2 fs-8 text-secondary-x-light"
        >
          <i class="bi bi-chat-square-fill" style="margin-top: 0.1rem"></i>
          <p class="m-0 p-0">{{ post.comments }}</p>
        </router-link>
        <router-link
          :to="{
            name: 'post-detail',
            params: { identifier: post.identifier },
          }"
          class="d-flex align-items-center gap-2 fs-9 text-secondary-x-light"
        >
          <i class="bi bi-bookmark-fill"></i>
          <p class="m-0 p-0">{{ post.bookmarks }}</p>
        </router-link>
      </div>

      <div class="d-flex align-items-center gap-2">
        <router-link
          :to="{
            name: 'post-detail',
            params: { identifier: post.identifier },
          }"
          class="text-secondary-x-light fs-7"
        >
          {{ post.category.name }}
        </router-link>
        <router-link
          v-for="filetype in post.filetypes"
          :key="filetype"
          :to="{
            name: 'post-detail',
            params: { identifier: post.identifier },
          }"
          class="text-light"
        >
          <i
            class="fs-5 text-secondary-x-light"
            :class="'bi bi-filetype-' + filetype"
          ></i>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, inject } from "vue";
import Tag from "@/components/Tag.vue";
import type PostModel from "@/models/PostModel";

// TODO: Figure out how to import extarnal libraries in Vue 3
const moment = inject("moment");

const props = defineProps({
  post: {
    type: Object as () => PostModel,
    required: true,
  },
});

const created_at = moment(props.post.created_at).fromNow();
</script>

<style scoped>
.btn-primary {
  border-color: var(--primary);
  color: var(--primary);
  background: transparent;
}

.btn-primary:hover {
  background: var(--primary);
  color: var(--secondary);
}
</style>
