<template>
  <div class="tablist">
    <ul class="nav nav-pills fs-6">
      <li class="nav-item">
        <button
          class="nav-link active"
          data-bs-toggle="pill"
          type="button"
          role="tab"
          aria-selected="true"
        >
          Все
        </button>
      </li>
      <li
        v-for="collection in collections"
        :key="collection.id"
        class="nav-item"
      >
        <button
          class="nav-link"
          data-bs-toggle="pill"
          type="button"
          role="tab"
          aria-selected="true"
        >
          {{ collection.name + " " + collection.emoji }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import type CollectionModel from "@/models/CollectionModel";
import { defineProps, onMounted } from "vue";

const props = defineProps({
  collections: Array as () => CollectionModel[],
});

onMounted(() => {
  console.log(props.collections);
});
</script>

<style scoped>
.tablist {
  width: 100%;
}

ul {
  width: 100%;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;

  /* --mask: linear-gradient(
      to Right,
      rgba(0, 0, 0, 1) 0,
      rgba(0, 0, 0, 1) 95%,
      rgba(0, 0, 0, 0) 99%,
      rgba(0, 0, 0, 0) 0
    )
    100% 50% / 100% 100% repeat-x;
  -webkit-mask: var(--mask);
  mask: var(--mask); */
}

.nav {
  flex-wrap: nowrap;
}

.nav-item {
  padding: 0.5rem 0.2rem !important;
  width: fit-content !important;
  border: 0 !important;
}

.nav-pills .nav-link.active {
  background-color: var(--primary);
  /* border-bottom: 1px solid var(--secondary) !important;
  border-right: 1px solid var(--secondary) !important; */
  color: var(--dark);
}

.nav-pills .nav-link {
  white-space: nowrap;
  border-radius: 0.4rem;
  font-weight: bold;
  padding: 0.3rem 0.8rem;
  background-color: var(--dark-light);
  color: var(--light);
  /* border-bottom: 1px solid var(--primary) !important;
  border-right: 1px solid var(--primary) !important; */
}
</style>
