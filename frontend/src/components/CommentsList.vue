<template>
  <div>
    <div v-for="comment in comments" :key="comment.identifier">
      <CommentItem :comment="comment" />
    </div>
  </div>
</template>

<script setup lang="ts">
import CommentItem from "@/components/CommentItem.vue";
import type CommentModel from "@/models/CommentModel";

const props = defineProps<{
  comments: CommentModel[];
}>();
</script>
