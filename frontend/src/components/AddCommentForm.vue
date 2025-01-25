<template>
  <div class="mt-5">
    <form @submit.prevent="addComment">
      <fieldset>
        <div class="mb-3">
          <label for="create-comment" class="form-label">Your Comment</label>
          <textarea
            v-model="content"
            id="create-comment"
            class="form-control"
            rows="3"
            placeholder="Write a comment..."
          ></textarea>
        </div>
        <button
          class="mb-2 btn border-start-0 border-top-0 btn-outline-primary mt-0 fs-8 action-unchecked"
          type="submit"
        >
          Submit
        </button>
      </fieldset>
    </form>
  </div>
</template>

<style></style>

<script setup lang="ts">
import { ref } from "vue";
import CommentsDataService from "@/services/CommentsDataService";
import { ProfileDetailModel } from "@/models/ProfileModel";
import { onMounted, defineProps } from "vue";

const props = defineProps({
  postId: {
    type: String,
    default: "",
  },
  profile: {
    type: Object as () => ProfileDetailModel,
    default: () => ({}),
  },
})

const content = ref("");

const addComment = async () => {
  console.log("Preparing to submit comment:", content.value);
  const commentData = {
    post: props.postId, 
    content: content.value,
  };

  try {
    await CommentsDataService.createComment(commentData);
    console.log("Comment submitted successfully");
    content.value = "";
  } catch (error) {
    console.error("Error submitting comment:", error);
  }
};



</script>
