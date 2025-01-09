<template>
  <div class="post card text-start bg-dark-light">
    <div
      class="post__header card-header d-flex flex-row align-items-center justify-content-between py-2"
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
        <div class="d-flex flex-column">
          <router-link
            :to="{
              name: 'profile',
              params: { username: post.author.username },
            }"
            class="link-primary fw-bold fs-6"
            style="height: 20px"
          >
            {{ post.author.username }}
          </router-link>
          <router-link
            :to="{
              name: 'post-detail',
              params: { identifier: post.identifier },
            }"
            class="btn-secondary-x-light fs-7"
          >
            {{ created_at }}
          </router-link>
        </div>
      </div>
      <div class="d-flex flex-row align-items-center gap-2">
        <!-- <i class="bi bi-dash btn-secondary-x-light"></i> -->

        <router-link
          :to="{
            name: 'post-detail',
            params: { identifier: post.identifier },
          }"
          class="btn-secondary-x-light fst-italic"
        >
          {{ post.category.name }}
        </router-link>
      </div>
    </div>

    <div class="card-body">
      <router-link
        :to="{
          name: 'post-detail',
          params: { identifier: post.identifier },
        }"
      >
        <h5 class="card-title text-light m-0">{{ post.title }}</h5>
      </router-link>
      <div class="d-flex flex-column">
        <div
          class="d-flex flex-row align-items-center gap-2"
          v-if="post.tags.length > 0"
        >
          <div class="d-flex flex-row gap-2">
            <Tag
              v-for="tag in post.tags"
              :key="tag.id"
              :tag="tag"
              class="mt-1"
            />
          </div>
        </div>
      </div>
      <img
        v-if="post.thumbnail"
        :src="post.thumbnail"
        class="card-img-top rounded-1 my-3"
        alt="post-thumbnail"
      />
      <p class="card-text text-light m-0">
        {{ post.description }}
        <span></span>
      </p>
      <router-link
        :to="{
          name: 'post-detail',
          params: { identifier: post.identifier },
        }"
        class="link-primary text-decoration-underline"
      >
        Читать далее...
      </router-link>
    </div>
    <div
      class="card-footer d-flex flex-row align-items-center justify-content-between p-3"
    >
      <div class="d-flex align-items-center gap-4">
        <router-link
          :to="{
            name: 'post-detail',
            params: { identifier: post.identifier },
          }"
          class="d-flex align-items-center gap-2 fs-8 btn-secondary-x-light"
        >
          <i class="bi bi-chat-square-fill" style="margin-top: 0.1rem"></i>
          <p class="m-0 p-0 fs-7">{{ post.comments_count }}</p>
        </router-link>
        <router-link
          :to="{
            name: 'post-detail',
            params: { identifier: post.identifier },
          }"
          class="d-flex align-items-center gap-2 fs-9 btn-secondary-x-light"
        >
          <i class="bi bi-bookmark-fill"></i>
          <p class="m-0 p-0 fs-7">{{ post.bookmarks_count }}</p>
        </router-link>
      </div>

      <div class="d-flex align-items-center gap-2">
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
import type PostListItemModel from "@/models/PostModel";

// TODO: Figure out how to import extarnal libraries in Vue 3
const moment = inject("moment") as any;

const props = defineProps({
  post: {
    type: Object as () => PostListItemModel,
    required: true,
  },
});

const created_at = moment(props.post.created_at).fromNow();
</script>

<style scoped>
/* .card:hover {
  border-bottom: 1px solid var(--secondary-light);
  border-right: 1px solid var(--secondary-light);
} */

/* .post:hover {
  border-bottom: 1px solid var(--primary) !important;
  border-right: 1px solid var(--primary) !important;
} */

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
