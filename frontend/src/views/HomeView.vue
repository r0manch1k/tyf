<template>
  <div class="home content open px-5" v-if="!loading">
    <!-- <div class="home__header mb-2">
      <Tablist v-bind:tablist="categories" />
      <CollectionsTablist v-bind:collections="collections" />
    </div> -->
    <div class="home__body container-fluid p-0">
      <div class="home__body__container row">
        <div class="home__body__container__left col-9">
          <div
            class="home__body__container__left__text d-flex flex-column gap-3 p-0"
          >
            <Post v-for="post in posts" :key="post.identifier" :post="post" />
          </div>
        </div>
        <div
          class="home__body__container__right col-3 d-flex flex-column gap-3"
        >
          <MostActiveUsersBar />
          <TyeHighscoresBar />
        </div>
      </div>
    </div>
  </div>
  <LoadingCircle v-else />
</template>

<script lang="ts" setup>
import LoadingCircle from "@/components/LoadingCircle.vue";
import CollectionsTablist from "@/components/CollectionsTablist.vue";
import MostActiveUsersBar from "@/components/MostActiveUsersBar.vue";
import TyeHighscoresBar from "@/tye_frontend/components/TyeHighscoresBar.vue";
import Post from "@/components/Post.vue";
import PostDataService from "@/services/PostDataService";
import type PostListItemModel from "@/models/PostModel";
import type CategoryModel from "@/models/CategoryModel";
import type CollectionModel from "@/models/CollectionModel";

import { ref, onMounted, computed, shallowRef } from "vue";
import { useStore } from "vuex";

const loading = ref(true);

const store = useStore();

const categories = computed<CategoryModel[]>(
  () => store.getters["category/getCategories"]
);
const collections = computed<CollectionModel[]>(
  () => store.getters["collection/getCollections"]
);
const posts = shallowRef<PostListItemModel[]>([]);

onMounted(async () => {
  await Promise.all([
    store.dispatch("category/fetchCategories"),
    store.dispatch("collection/fetchCollections"),
    (posts.value = await PostDataService.getAllPosts()),
  ]).then(() => {
    loading.value = false;
  });
});
</script>

<style>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.home__header {
  width: 100%;
  margin-right: auto;
}
</style>
