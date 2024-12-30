<template>
  <div class="home content open px-5 py-2" v-if="!loading">
    <div class="home__header">
      <Tablist v-bind:tablist="categories" />
      <!-- <Tablist v-bind:tablist="collections" /> -->
    </div>
    <div class="home__body">
      <div class="home__body__container">
        <div class="home__body__container__left">
          <div class="home__body__container__left__text">
            <h1>Latest Posts</h1>
            <Post v-for="post in posts" :key="post.identifier" :post="post" />
          </div>
        </div>
      </div>
    </div>
  </div>
  <LoadingCircle v-else />
</template>

<script lang="ts" setup>
import LoadingCircle from "@/components/LoadingCircle.vue";
import Tablist from "@/components/Tablist.vue";
import Post from "@/components/Post.vue";
import PostDataService from "@/stores/services/PostDataService";
import { ref, onMounted, computed, shallowRef } from "vue";
import { useStore } from "vuex";

const loading = ref(true);

const store = useStore();

const categories = computed(() => store.getters["category/getCategories"]);
const collections = computed(() => store.getters["collection/getCollections"]);
import type PostModel from "@/models/PostModel";

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
