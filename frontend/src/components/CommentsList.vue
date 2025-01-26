<template>
  <div>
    <div v-for="comment in comments" :key="comment.identifier">
      <CommentItem
        :comment="comment"
        @deleteComment="deleteComment"
        :profile="profile"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
// import { defineEmits } from "vue";
import { ref } from "vue";
import CommentItem from "@/components/CommentItem.vue";
import type CommentModel from "@/models/CommentModel";
import type ProfileModel from "@/models/ProfileModel";

const props = defineProps<{
  comments: CommentModel[];
  profile: ProfileModel;
}>();

// const emit = defineEmits();
const comments = ref<CommentModel[]>(props.comments);

const deleteComment = (identifier: string) => {
  const commentIndex = comments.value.findIndex(
    (comment) => comment.identifier === identifier
  );
  if (commentIndex !== -1) {
    comments.value.splice(commentIndex, 1);
  }
};


</script>
