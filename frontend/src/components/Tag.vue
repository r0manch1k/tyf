<template>
  <router-link :to="{ name: 'home' }" class="tag">
    <span class="tag__container" :style="'background-color: ' + tag.color">
      <span class="tag__content fs-7">{{ tag.name }}</span>
    </span>
  </router-link>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import type TagModel from "@/models/TagModel";

const props = defineProps({
  tag: {
    type: Object as () => TagModel,
    required: true,
  },
});
</script>

<style scoped>
.tag__container {
  display: inline-block !important;
}
.tag__content {
  filter: invert(1) !important;
  display: inline-block !important;
  font-weight: bold;
}
</style>
