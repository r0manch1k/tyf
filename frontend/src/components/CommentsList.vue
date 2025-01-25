<template>
  <div>
    <div v-for="comment in comments" :key="comment.identifier">
      <CommentItem :comment="comment" @deleteComment="deleteComment" />

    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import CommentItem from "@/components/CommentItem.vue";
import type CommentModel from "@/models/CommentModel";

const props = defineProps<{
  comments: CommentModel[];
}>();

const deleteComment = (identifier: string) => {
  const index = props.comments.findIndex((comment) => comment.identifier === identifier);
  if (index !== -1) {
    props.comments.splice(index, 1);
  }
};

</script>
