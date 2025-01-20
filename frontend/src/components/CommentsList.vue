<template>
  <div>
    <div v-for="comment in comments" :key="comment.identifier">
      <CommentItem :comment="comment" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import CommentItem from "@/components/CommentItem.vue";
import type CommentModel from "@/models/CommentModel";

defineProps<{
  comments: CommentModel[];
}>();
</script>
