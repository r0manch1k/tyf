<template>
  <div class="mt-5">
    <h5 class="mb-4 fs-6">Comments</h5>
    <hr />
    <div v-if="comments.length > 0" class="nested-comments">
      <ul id="comment-thread" class="ps-0">
        <!-- TODO: P.S. removed index from v-for -->
        <li
          v-for="comment in comments"
          :key="comment.id"
          class="d-flex flex-column mb-2"
          :style="{ marginLeft: comment.level + 'em' }"
        >
          <div class="d-flex">
            <div style="margin-right: 0.5rem">
              <a :href="'/profile/' + comment.author.username">
                <img
                  :src="comment.author.avatar"
                  :alt="comment.author.username"
                  class="rounded-circle"
                  style="width: 50px; height: 50px"
                />
              </a>
            </div>
            <div class="flex-grow-1">
              <div
                class="mt-1 d-flex justify-content-between align-items-center"
              >
                <a
                  :href="'/profile/' + comment.author.username"
                  class="text-light mb-1 fs-7"
                >
                  {{ comment.author.username }}
                </a>
                <div class="d-flex align-items-center">
                  <button
                    v-if="isAuthenticated"
                    class="border-0 text-muted bg-transparent d-block ml-auto reply-btn comments__reply"
                  >
                    <i class="bi bi-reply-fill" style="font-size: 15px"></i>
                  </button>
                  <button
                    v-if="isAuthenticated && comment.author.isCurrentUser"
                    class="ms-1 border-0 text-muted bg-transparent d-block"
                  >
                    <i class="bi bi-trash-fill" style="font-size: 12px"></i>
                  </button>
                  <button
                    v-if="isAuthenticated && comment.author.isCurrentUser"
                    class="ms-1 border-0 text-muted bg-transparent d-block edit-btn"
                  >
                    <i
                      class="bi bi-pencil-square"
                      style="font-size: 12.5px"
                    ></i>
                  </button>
                  <small class="text-muted fs-9 ms-2">
                    {{ new Date(comment.createdAt).toLocaleString() }}
                  </small>
                </div>
              </div>
              <p class="fs-8 mb-1">{{ comment.content }}</p>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <p v-else class="text-muted fs-7">No comments yet.</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
// import { defineComponent } from "vue";

interface Author {
  id: number;
  username: string;
  avatar: string;
  isCurrentUser: boolean;
}

interface Comment {
  id: number;
  content: string;
  level: number;
  createdAt: string;
  author: Author;
}

const isAuthenticated = ref(true);

const comments = ref<Comment[]>([
  {
    id: 1,
    content: "This is a comment.",
    level: 0,
    createdAt: "2024-12-20T10:00:00Z",
    author: {
      id: 1,
      username: "john_doe",
      avatar: "/path/to/avatar.jpg",
      isCurrentUser: true,
    },
  },
  {
    id: 2,
    content: "This is a reply.",
    level: 1,
    createdAt: "2024-12-20T11:00:00Z",
    author: {
      id: 2,
      username: "jane_doe",
      avatar: "/path/to/avatar2.jpg",
      isCurrentUser: false,
    },
  },
]);
</script>
