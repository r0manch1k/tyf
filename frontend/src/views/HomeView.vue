<template>
  <div class="home content open px-5" v-if="!loading" ref="scrollComponent">
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
            <LoadingCircle v-if="isFetching" />
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
import MostActiveUsersBar from "@/components/MostActiveUsersBar.vue";
import Post from "@/components/Post.vue";
import type PostListItemModel from "@/models/PostModel";
import PostDataService from "@/services/PostDataService";
import TyeHighscoresBar from "@/tye_frontend/components/TyeHighscoresBar.vue";
// import CollectionsTablist from "@/components/CollectionsTablist.vue";
// import type CategoryModel from "@/models/CategoryModel";
// import type CollectionModel from "@/models/CollectionModel";

import { onMounted, onUnmounted, ref } from "vue";
import { useStore } from "vuex";
// import { computed } from "vue";

const scrollComponent = ref<HTMLElement | null>(null);
const posts = ref<PostListItemModel[]>([]);
const isFetching = ref(false);
const loading = ref(true);
const store = useStore();

// const categories = computed<CategoryModel[]>(
//   () => store.getters["category/getCategories"]
// );
// const collections = computed<CollectionModel[]>(
//   () => store.getters["collection/getCollections"]
// );

const fetchNewPosts = async () => {
  if (isFetching.value) return;
  isFetching.value = true;

  try {
    const newPosts = await PostDataService.getPosts();
    posts.value.push(...newPosts);
  } catch (error) {
    console.error(error);
  } finally {
    isFetching.value = false;
  }
};

const handleScroll = () => {
  let element = scrollComponent.value;

  if (element) {
    if (element.getBoundingClientRect().bottom < window.innerHeight * 1.5) {
      fetchNewPosts();
    }
  }
};

onMounted(async () => {
  store.commit("pagination/enablePostsFetching");
  await Promise.all([
    store.dispatch("profile/fetchProfile"),
    store.dispatch("category/fetchCategories"),
    store.dispatch("collection/fetchCollections"),
    (posts.value = await PostDataService.getPosts()),
  ]).then(() => {
    loading.value = false;
  });
  document.getElementById("app")?.addEventListener("scroll", handleScroll);
});

onUnmounted(() => {
  document.getElementById("app")?.removeEventListener("scroll", handleScroll);
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
