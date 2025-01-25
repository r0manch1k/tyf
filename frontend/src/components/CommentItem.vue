<template>
  <div class="comment p-3">
    <div class="d-flex gap-2 align-items-center">
      <router-link :to="'/' + comment.author.username">
        <img
          :src="comment.author.avatar"
          alt="avatar"
          class="rounded-circle"
          style="width: 40px; height: 40px"
        />
      </router-link>
      <div class="d-flex flex-column text-start">
        <router-link
          :to="'/' + comment.author.username"
          class="text-light"
        >
          {{ comment.author.username }}
        </router-link>
        <span class="text-muted fs-9">{{ comment.created_at }}</span>
      </div>
      <button
        class="btn btn-danger btn-sm ms-auto"
        v-if="profile.username === comment.author.username"
        @click="deleteComment"
        >delete</button>
      <!-- Edit -->
      <!-- <button -->
      <!--   class="btn btn-warning btn-sm ms-2" -->
      <!--   v-if="profile.username === comment.author.username" -->
      <!--   >edit</button> -->
      <EditCommentForm :comment="comment" /> 
      <ReplyCommentForm :comment="comment" @submitReply="addReply" /> 
    </div>
    <p class="text-light mt-2 text-start">{{ comment.content }}</p>
    <div v-if="comment.replies.length > 0" class="nested-comments ms-4">
      <div v-for="reply in comment.replies" :key="reply.identifier">
        <CommentItem :comment="reply" :profile="profile" @addReply="addReply" /> 
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import type CommentModel from "@/models/CommentModel";
import CommentsDataService from "@/services/CommentsDataService";
import ProfileModel from "@/models/ProfileModel";
import EditCommentForm from "@/components/EditCommentForm.vue";
import ReplyCommentForm from "@/components/ReplyCommentForm.vue";


const props = defineProps<{
  comment: CommentModel;
  profile: ProfileModel;
}>();

const emit = defineEmits();

const deleteComment = async () => {
  await CommentsDataService.deleteCommentByIdentifier(props.comment.identifier);
  emit("deleteComment", props.comment.identifier); 
};

const addReply = (reply: CommentModel) => {
  reply.author = props.profile;
  props.comment.replies.push(reply);
};


</script>

<style scoped>
.comment {
  border-left: #ffffff 1px solid;
}

.nested-comments {
  margin-left: 20px;
}
</style>
