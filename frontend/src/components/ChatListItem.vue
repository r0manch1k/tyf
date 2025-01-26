<template>
  <div class="chat-list-item">
    <div class="chat-list-item__container">
      <div class="chat-list-item__chat">
        <div class="chat-list-item__chat-avatar">
          <img
            class="chat-list-item__chat-avatar-img rounded-circle"
            :src="chat.thumbnail"
          />
        </div>
        <div class="chat-list-item__chat-info">
          <div class="chat-list-item__chat-name">{{ chat.name }}</div>
          <div class="chat-list-item__chat-last-message">
            {{ chat.last_message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, defineProps } from "vue";
import type { ChatListItemModel } from "@/models/ChatModel";

const props = defineProps<{
  chat: ChatListItemModel;
}>();

const chat = ref<ChatListItemModel>(props.chat);
</script>
