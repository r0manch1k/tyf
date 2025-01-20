<template>
  <div class="most-bookmarked-posts-bar bg-dark-light p-1">
    <div class="most-bookmarked-posts-bar__content" v-if="!loading">
      <h3
        class="most-bookmarked-posts-bar__title fs-6 text-light p-1 m-0 text-start text-decoration-none"
      >
        <span class="text-decoration-underline">Самые полезные посты</span>
        <span class="most-bookmarked-posts-bar__emoji"> 📚</span>
      </h3>

      <h4
        class="most-bookmarked-posts-bar__subtitle fs-6 text-secondary-xx-light p-1 m-0 fw-normal text-start"
      >
        Посты с наибольшим количеством сохранений
      </h4>

      <table
        class="most-bookmarked-posts-bar__table table table-dark-light table-striped"
      >
        <thead>
          <tr class="most-bookmarked-posts-bar__table-header">
            <th
              scope="col"
              class="most-bookmarked-posts-bar__table-header-cell text-start fw-normal"
            >
              Пост
            </th>
            <th
              scope="col"
              class="most-bookmarked-posts-bar__table-header-cell fw-normal"
            >
              Сохранения
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="post in posts"
            :key="post.identifier"
            class="most-bookmarked-posts-bar__table-row"
          >
            <td
              class="most-bookmarked-posts-bar__table-cell align-middle text-start"
            >
              <router-link
                :to="{
                  name: 'post-detail',
                  params: { identifier: post.identifier },
                }"
                class="most-bookmarked-posts-bar__link btn-light fs-6 text-decoration-none text-primary"
              >
                {{ post.title }}
              </router-link>
            </td>
            <td class="most-bookmarked-posts-bar__table-cell align-middle">
              <router-link
                :to="{
                  name: 'post-detail',
                  params: { identifier: post.identifier },
                }"
                class="most-bookmarked-posts-bar__link btn-light fs-6 text-decoration-none"
              >
                {{ post.bookmarks_count }}
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <LoadingCircle
      v-else
      class="most-bookmarked-posts-bar__loading-spinner spinner-border-sm"
    />
  </div>
</template>

<script setup lang="ts">
import LoadingCircle from "@/components/LoadingCircle.vue";
import PostDataService from "@/services/PostDataService";
import type PostListItemModel from "@/models/PostModel";
import { ref, onMounted } from "vue";

const posts = ref<PostListItemModel[]>([]);
const loading = ref(true);

onMounted(async () => {
  posts.value = await PostDataService.getMostBookmarkedPosts();
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

.most-bookmarked-posts-bar {
  border-radius: 0.4rem;
  /* border: 1px solid var(--secondary); */
}
</style>
