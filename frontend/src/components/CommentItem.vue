<template>
  <div class="comment p-3">
    <div class="d-flex gap-2 align-items-center">
      <router-link :to="'/profile/' + comment.author.username">
        <img
          src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCpkMGWpU-ODFuq82EYaQElelh62mKO5VREQ&s"
          alt="avatar"
          class="rounded-circle"
          style="width: 40px; height: 40px"
        />
      </router-link>
      <div class="d-flex flex-column text-start">
        <router-link
          :to="'/profile/' + comment.author.username"
          class="text-light"
        >
          Username
        </router-link>
        <span class="text-muted fs-9">{{ comment.created_at }}</span>
      </div>
    </div>
    <p class="text-light mt-2 text-start">{{ comment.content }}</p>

    <div v-if="comment.replies.length > 0" class="nested-comments ms-4">
      <div v-for="reply in comment.replies" :key="reply.identifier">
        <CommentItem :comment="reply" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import type CommentModel from "@/models/CommentModel";

defineProps<{
  comment: CommentModel;
}>();
</script>

<style scoped>
.comment {
  border-left: #ffffff 1px solid;
}

.nested-comments {
  margin-left: 20px;
}
</style>
