<template>
  <div class="home content open px-5 py-2" v-if="!loading">
    <div class="home__header mb-2">
      <Tablist v-bind:tablist="categories" />
      <!-- <Tablist v-bind:tablist="collections" /> -->
    </div>
    <div class="home__body container-fluid p-0">
      <div class="home__body__container row">
        <div class="home__body__container__left col-9">
          <div class="home__body__container__left__text p-0">
            <Post v-for="post in posts" :key="post.identifier" :post="post" />
          </div>
        </div>
        <div class="home__body__container__right col-3"></div>
      </div>
    </div>
  </div>
  <LoadingCircle v-else />
</template>

<script lang="ts" setup>
import LoadingCircle from "@/components/LoadingCircle.vue";
import Tablist from "@/components/Tablist.vue";
import Post from "@/components/Post.vue";
import PostDataService from "@/services/PostDataService";
import type PostModel from "@/models/PostModel";
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
const posts = shallowRef<PostModel[]>([]);

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
