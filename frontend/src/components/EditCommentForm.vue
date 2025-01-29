<template>
  <form id="edit-form" class="mt-4" @submit.prevent="updateComment">
    <fieldset>
      <div class="mb-3">
        <label for="edit-comment" class="form-label">Edit Comment</label>
        <textarea
          v-model="content"
          id="edit-comment"
          class="form-control"
          rows="3"
          placeholder="Edit your comment..."
        ></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Save Changes</button>
      <button type="button" class="btn btn-secondary cancel-edit">
        Cancel
      </button>
    </fieldset>
  </form>
</template>

<style></style>

<script setup lang="ts">
import CommentsDataService from "@/services/CommentsDataService";
import type CommentPayload from "@/models/CommentPayload";
import { defineEmits, defineProps, ref } from "vue";

const content = ref("");
const emit = defineEmits(["updateComment"]);
const props = defineProps({
  postId: {
    type: String,
    default: "",
  },
  comment: {
    type: Object,
    default: () => ({}),
  },
});

const updateComment = async () => {
  const commentData: CommentPayload = {
    post: props.postId,
    content: content.value,
  };

  try {
    const updatedComment = await CommentsDataService.updateCommentByIdentifier(
      props.comment.identifier,
      commentData
    );
    emit("updateComment", updatedComment);
    content.value = "";
  } catch (error) {
    console.error("Error updating comment:", error);
  }
};
</script>
