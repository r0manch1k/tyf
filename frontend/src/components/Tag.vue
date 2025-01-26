<template>
  <div class="tag">
    <span class="tag__container" :style="'background-color: ' + tag.color">
      <a
        @click="enableSearch(tag.name.substring(1))"
        class="tag__content fs-8"
        >{{ tag.name }}</a
      >
    </span>
  </div>
</template>

<script setup lang="ts">
import type TagModel from "@/models/TagModel";
import { defineProps } from "vue";
import { useStore } from "vuex";

const store = useStore();

const enableSearch = (name: string) => {
  store.dispatch("pagination/updateSearchInput", {
    query: name.trim(),
    method: "tag",
  });
};

defineProps({
  tag: {
    type: Object as () => TagModel,
    required: true,
  },
});
</script>

<style scoped>
/* .tag__container {
  display: inline-block !important;
} */
.tag__content {
  filter: invert(1) !important;
  display: inline-block !important;
  font-weight: bold;
  cursor: pointer !important;
}
</style>
