<template>
  <div class="home content open px-5" v-if="!loading" ref="scrollComponent">
    <div class="home__header mb-2">
      <!-- <Tablist v-bind:tablist="categories" /> -->
      <CollectionsTablist v-if="!searchInput.query" v-bind:collections="collections" />
    </div>
    <div class="home__body container-fluid p-0">
      <div class="home__body__container row">
        <div class="home__body__container__left col-9">
          <div
            class="home__body__container__left__text d-flex flex-column gap-3 p-0"
          >
            <SearchInfo
              v-if="showSearchInfo"
              :search-info="searchInput"
              :results-count="resultsCount"
            />
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
import SearchInfo from "@/components/SearchInfo.vue";
import type PostListItemModel from "@/models/PostModel";
import type SearchModel from "@/models/SearchModel";
import PostDataService from "@/services/PostDataService";
import TyeHighscoresBar from "@/tye_frontend/components/TyeHighscoresBar.vue";
import CollectionsTablist from "@/components/CollectionsTablist.vue";
// import type CategoryModel from "@/models/CategoryModel";
import type CollectionModel from "@/models/CollectionModel";
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useStore } from "vuex";

const store = useStore();

const loading = ref(true);
const resultsCount = ref(0);
const isFetching = ref(false);
const showSearchInfo = ref(false);
const posts = ref<PostListItemModel[]>([]);
const scrollComponent = ref<HTMLElement | null>(null);

const searchInput = computed<SearchModel>(
  () => store.state.pagination.searchInput
);
// const categories = computed<CategoryModel[]>(
//   () => store.getters["category/getCategories"]
// );
const collections = computed<CollectionModel[]>(
  () => store.getters["collection/getCollections"]
);

let searchTimeout: ReturnType<typeof setTimeout> | null = null;

const onSearchInputChange = () => {
  posts.value = [];
  showSearchInfo.value = false;
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }

  searchTimeout = setTimeout(() => {
    store.commit("pagination/enablePostsFetching");
    fetchNewPosts();
  }, 800);
};

const fetchNewPosts = async () => {
  if (isFetching.value) return;
  isFetching.value = true;

  try {
    let response;
    if (searchInput.value.query) {
      response = await PostDataService.getPosts(
        searchInput.value.query,
        searchInput.value.method
      );
      resultsCount.value = response.count;
      showSearchInfo.value = true;
    } else {
      response = await PostDataService.getPosts();
      showSearchInfo.value = false;
    }

    posts.value.push(...response.posts);
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
    (posts.value = (await PostDataService.getPosts()).posts),
  ]).then(() => {
    loading.value = false;
  });
  document.getElementById("app")?.addEventListener("scroll", handleScroll);
});

onUnmounted(() => {
  document.getElementById("app")?.removeEventListener("scroll", handleScroll);
});

watch(searchInput.value, () => {
  onSearchInputChange();
});
</script>

<style>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;
}

.home__header {
  width: 100%;
  margin-right: auto;
}
</style>
