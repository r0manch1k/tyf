<template>
  <div class="message-chat>">
    <div class="message-chat__container">
      <div class="message-chat__chat">
        <div class="message-chat__chat-info">
          <div class="message-chat__chat-last-message">
            {{ message.text }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { defineProps } from "vue";
import type MessageChatModel from "@/models/MessageChatModel";

const props = defineProps<{
  message: MessageChatModel;
}>();
</script>
