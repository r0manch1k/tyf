<template>
  <div class="home content open" v-if="!loading">
    <div class="home__header">
      <TablistHome v-bind:categories="categories" />
    </div>
    <div class="home__body">
      <div class="home__body__container">
        <div class="home__body__container__left">
          <div class="home__body__container__left__text"></div>
        </div>
      </div>
    </div>
  </div>
  <LoadingCircle v-else />
</template>

<script lang="ts" setup>
import LoadingCircle from "@/components/LoadingCircle.vue";
import TablistHome from "@/components/TablistHome.vue";
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";

const loading = ref(true);

const store = useStore();

const categories = computed(() => store.getters["category/getCategories"]);

onMounted(async () => {
  // Promise.all([store.dispatch("main/getCategories")]).then(() => {
  //   loading.value = false;
  // });
  await store.dispatch("category/fetchCategories");
  loading.value = false;
});
</script>

<style scoped></style>
