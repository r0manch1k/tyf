<template>
  <div v-if="!loading" class="h-100 p-4">
    <div
      class="card rounded-0 border-top-0 border-bottom-0 bg-transparent border-light p-4"
      style="border-left: 0 !important; border-right: 0 !important"
    >
      <div class="row flex-md-row">
        <!-- Левая колонка с аватаром и информацией -->
        <div class="mb-3 mb-md-0 flex-shrink-0">
          <div class="d-flex align-items-center gap-2">
            <router-link :to="'/profile/' + post.author.username">
              <img
                :src="post.author.avatar"
                alt="avatar"
                class="img-fluid rounded-circle"
                style="width: 50px; height: 50px"
              />
            </router-link>
            <div class="d-flex flex-column">
              <router-link
                :to="'/profile/' + post.author.username"
                class="text-light fs-6 mb-1"
              >
                {{ post.author.username }}
              </router-link>
              <span class="fs-9 text-muted">
                <i class="bi bi-calendar3 me-1"></i>{{ post.createdAt }}
              </span>
            </div>
          </div>

          <hr />

          <div class="d-flex justify-content-between align-items-center">
            <h1 class="post-title text-light fs-4 h1-super">
              {{ post.title }}
            </h1>
            <div class="d-flex gap-3 align-items-center">
              <button
                v-if="isEditable"
                @click="editPost"
                class="text-light border-0 bg-transparent"
              >
                <i class="bi bi-pencil-square fs-6"></i>
              </button>
              <button
                v-if="isEditable"
                @click="deletePost"
                class="text-light border-0 bg-transparent"
              >
                <i class="bi bi-trash-fill" style="font-size: 15px"></i>
              </button>
              <button
                @click="toggleBookmark"
                class="text-light border-0 bg-transparent"
              >
                <i
                  :class="[
                    'bi',
                    isBookmarked ? 'bi-bookmark-fill' : 'bi-bookmark',
                  ]"
                ></i>
              </button>
            </div>
          </div>

          <div class="post-info d-flex gap-3 text-muted">
            <span class="fs-9">
              <a href="#" class="text-muted fs-9">
                <i class="bi bi-collection me-1"></i>{{ post.category }}
              </a>
            </span>
            <span class="fs-9">
              <i class="bi bi-eye me-1"></i>{{ post.views }}
            </span>
            <span class="fs-9">
              <a href="#attachments" class="text-muted fs-9">
                <i class="bi bi-paperclip"></i>{{ post.media.length }}
                files
              </a>
            </span>
          </div>

          <div
            class="post-description rounded bg-dark-subtle text-light fs-6 mt-4"
          >
            <p>{{ post.content }}</p>
          </div>

          <hr id="attachments" />

          <div class="fs-9">
            <span
              v-for="tag in post.tags"
              :key="tag"
              class="badge bg-secondary fs-9"
            >
              {{ tag }}
            </span>
          </div>

          <br />

          <div v-if="post.media.length">
            <h5 class="mt-3 fs-6" id="comments">Attachments:</h5>
            <ul class="attachments-list list-unstyled fs-8">
              <li v-for="file in post.media" :key="file.id">
                <i class="bi" :class="'bi-filetype-' + file.type + ' fs-6'"></i>
                <a :href="file.url" target="_blank" class="mb-2 mt-2 fs-8">
                  {{ file.name }}
                </a>
              </li>
            </ul>
          </div>

          <hr />

          <!-- Comments Section -->
          <Comments :comments="post.comments" />
        </div>
      </div>
    </div>
  </div>
  <LoadingCircle v-else />
</template>

<script setup lang="ts">
import { ref, defineProps, onMounted } from "vue";
import LoadingCircle from "@/components/LoadingCircle.vue";
import PostDataService from "@/services/PostDataService";
import type PostModel from "@/models/PostModel";

const props = defineProps({
  identifier: String,
});

const post = ref<PostModel | null>(null);
const loading = ref(true);

onMounted(async () => {
  post.value = await PostDataService.getPostByIdentifier(props.identifier);
  loading.value = false;
});


</script>

<style></style>
