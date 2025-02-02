<template>
  <div class="text-center mt-0" style="color: var(--light)">
    <svg
      class="me-3"
      xmlns="http://www.w3.org/2000/svg"
      width="16"
      height="16"
      fill="currentColor"
      viewBox="0 0 16 16"
    >
      <path
        d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"
      />
    </svg>
    <span v-if="searchInfo.method === 'full'"
      >Результаты поиска постов по запросу: "{{ searchInfo.query }}".
    </span>
    <span v-else-if="searchInfo.method === 'tag'"
      >Результаты поиска постов по тегу: "#{{ searchInfo.query }}".
    </span>
    <span v-else-if="searchInfo.method === 'category'"
      >Результаты поиска постов по категории: "{{ searchInfo.query }}".
    </span>
    <span v-else-if="searchInfo.method === 'collection'"
      >Результаты поиска постов по коллекции: "{{ searchInfo.query }}".
    </span>
    <span v-else-if="searchInfo.method === 'author'"
      >Результаты поиска постов по имени автора: "{{ searchInfo.query }}".
    </span>
    <span v-else-if="searchInfo.method === 'title'"
      >Результаты поиска постов по заголовку: "{{ searchInfo.query }}".
    </span>
    <span>Количество найденных постов: {{ resultsCount }}. </span>
    <hr />
  </div>
</template>

<script lang="ts" setup>
import type SearchModel from "@/models/SearchModel";
import { defineProps } from "vue";

defineProps({
  searchInfo: {
    type: Object as () => SearchModel,
    required: true,
  },
  resultsCount: {
    type: Number,
    default: 0,
  },
});
</script>
