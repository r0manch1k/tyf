<template>
  <form id="reply-form" class="mt-4" @submit.prevent="submitReply">
    <fieldset>
      <div class="mb-3">
        <label for="reply-comment" class="form-label">Your Reply</label>
        <textarea
          v-model="replyContent"
          id="reply-comment"
          class="form-control"
          rows="3"
          placeholder="Write a reply..."
        ></textarea>
      </div>
      <button
        type="submit"
        class="mb-2 btn border-start-0 border-top-0 btn-outline-primary mt-2 action-unchecked comments__reply"
      >
        Submit Reply
      </button>
    </fieldset>
  </form>
</template>

<style></style>

<script setup lang="ts">
import { ref } from "vue";
import { defineProps, defineEmits } from "vue"; // Импортируйте defineEmits
import CommentsDataService from "@/services/CommentsDataService";

const replyContent = ref("");

// Определите свойства
const props = defineProps({
  comment: {
    type: Object,
    default: () => ({}),
  },
});

const emit = defineEmits(["submitReply"]);

async function submitReply() {
  console.log("Preparing to submit reply...");
  const replyData = {
    post: props.comment.post,
    content: replyContent.value, 
    parent: props.comment.identifier,
  };

  try {
    const newReply = await CommentsDataService.createReply(replyData);
    console.log("Reply submitted:", newReply);
    emit("submitReply", newReply); 
  } catch (error) {
    console.error("Error submitting reply:", error);
  }
}
</script>
