<template>
  <div class="tablist">
    <ul class="nav nav-pills">
      <li class="nav-item me-2">
        <button
          @click="disableSearch"
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
        class="nav-item me-2"
      >
        <button
          @click="enableSearch(collection.name)"
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
import { defineProps } from "vue";
import { useStore } from "vuex";

const store = useStore();

const enableSearch = (name: string) => {
  store.dispatch("search/updateSearchInput", {
    query: name.trim(),
    method: "collection",
  });
};

const disableSearch = () => {
  store.dispatch("search/updateSearchInput", {
    query: "",
    method: "full",
  });
};

defineProps({
  collections: Array as () => CollectionModel[],
});
</script>

<style scoped>
.tablist {
  max-width: 100%;
  max-height: 200px;
  overflow-x: auto;
  /* scrollbar-width: thin; */
  scrollbar-color: rgba(255, 255, 255, 0) transparent;
  transition: scrollbar-color 0.15s ease-in-out;
}

.tablist:hover {
  scrollbar-color: rgba(255, 255, 255, 0.5) transparent;
}

.tablist::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.tablist::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0);
  border-radius: 4px;
  -webkit-transition: background-color 0.15s ease-in-out;
}

.tablist:hover::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.5);
}

.tablist::-webkit-scrollbar-track {
  background: transparent;
  border: none;
}

ul {
  width: 100%;
  padding: 0;
  margin: 0;
  list-style-type: none;
}

.nav {
  flex-wrap: nowrap;
}

.nav-item {
  padding: 0 0.3rem !important;
  width: fit-content !important;
  border: 0 !important;
}

.nav-pills .nav-link.active {
  background-color: var(--primary);
  color: var(--dark);
}

.nav-pills .nav-link {
  white-space: nowrap;
  border-radius: 0.4rem;
  padding: 0.3rem 0.8rem;
  background-color: var(--dark-light);
  color: var(--light);
}
</style>
