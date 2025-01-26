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
  store.dispatch("pagination/updateSearchInput", {
    query: name.trim(),
    method: "collection",
  });
};

const disableSearch = () => {
  store.dispatch("pagination/updateSearchInput", {
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
  width: 100%;
  overflow-y: hidden;
  scrollbar-width: none;
  transition: scrollbar-width 1s linear;
}

.tablist:hover {
  overflow-y: auto !important;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.5) transparent;
  max-height: 200px;
}

/*
.tablist ul {
  padding: 0;
  margin: 0;
  list-style: none;
} */

.tablist::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.tablist::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
}

.tablist::-webkit-scrollbar-track {
  background: transparent;
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
  padding: 0.5rem 0.2rem !important;
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
  font-weight: bold;
  padding: 0.3rem 0.8rem;
  background-color: var(--dark-light);
  color: var(--light);
}
</style>
