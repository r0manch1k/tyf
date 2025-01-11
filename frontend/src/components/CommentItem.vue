<template>
  <div class="comment mt-3 p-3 border rounded">
    <!-- Информация о комментарии -->
    <div class="d-flex gap-2 align-items-center">
      <router-link :to="'/profile/' + comment.author.username">
        <img
          :src="comment.author.avatar"
          alt="avatar"
          class="rounded-circle"
          style="width: 40px; height: 40px"
        />
      </router-link>
      <div>
        <router-link
          :to="'/profile/' + comment.author.username"
          class="text-light"
        >
          {{ comment.author.username }}
        </router-link>
        <span class="text-muted fs-9">{{ comment.created_at }}</span>
      </div>
    </div>
    <p class="text-light mt-2">{{ comment.content }}</p>

    <!-- Вложенные комментарии (если есть) -->
    <div v-if="comment.replies.length > 0" class="nested-comments mt-3 ms-4">
      <div v-for="reply in comment.replies" :key="reply.identifier">
        <CommentItem :comment="reply" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CommentModel } from "@/models/CommentModel";

const props = defineProps<{
  comment: CommentModel;
}>();
</script>

<style scoped>
.comment {
  background-color: #1d1d1d;
  color: #fff;
}

.nested-comments {
  margin-left: 20px;
}
</style>
