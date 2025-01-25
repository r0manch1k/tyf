<template>
  <div>
    <div v-for="comment in comments" :key="comment.identifier">
      <CommentItem :comment="comment" @deleteComment="deleteComment" :profile="profile" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import CommentItem from "@/components/CommentItem.vue";
import type CommentModel from "@/models/CommentModel";
import type ProfileModel from "@/models/ProfileModel";

const props = defineProps<{
  comments: CommentModel[];
  profile: ProfileModel;
}>();

const deleteComment = (identifier: string) => {
  const index = props.comments.findIndex((comment) => comment.identifier === identifier);
  if (index !== -1) {
    props.comments.splice(index, 1);
  }
};

</script>
