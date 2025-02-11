<template>
  <div
    class="message-chat d-flex align-items-center gap-2"
    :class="{ 'message-chat__my': isMyMessage }"
  >
    <div class="message-chat__chat-avatar">
      <router-link
        :to="{
          name: 'profile',
          params: { username: message.author.username },
        }"
        v-if="!isMyMessage"
      >
        <img
          :src="message.author.avatar"
          alt="thumbnail"
          class="message-chat__chat-avatar-img rounded-circle"
          style="width: 30px; height: 30px"
        />
      </router-link>
    </div>
    <div
      class="message-chat__chat-container-a d-flex flex-column"
      :class="{ 'message-chat-chat-container-a__my': isMyMessage }"
    >
      <div
        class="message-chat__container"
        :class="{ 'message-chat__container__my': isMyMessage }"
      >
        <div class="message-chat__chat">
          <div class="message-chat__chat-info">
            <div class="message-chat__chat-message">
              {{ message.text }}
            </div>
          </div>
        </div>
      </div>
      <div
        class="message-chat__chat-time"
        :class="{ 'message-chat__chat-time__my': isMyMessage }"
      >
        <p class="text-secondary-xx-light fs-8 m-0">{{ created_at }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { defineProps, computed } from "vue";
import { useStore } from "vuex";
import type MessageChatModel from "@/models/MessageChatModel";
import moment from "moment";
import "moment/locale/ru";

const props = defineProps<{
  message: MessageChatModel;
}>();

const store = useStore();

const profile = computed(() => store.getters["profile/getProfile"]);

const isMyMessage = computed(
  () => props.message.author.username === profile.value.username
);

const created_at = computed(() =>
  moment(props.message.created_at).locale("ru").fromNow()
);
</script>

<style scoped>
.message-chat__my {
  margin-left: auto;
}

.message-chat__container {
  background-color: var(--dark-x-light);
  padding: 0.25rem 0.5rem;
  border-radius: 0.4rem;
  border-bottom-left-radius: 0;
  width: fit-content;
}

.message-chat__container__my {
  border-radius: 0.4rem;
  border-bottom-right-radius: 0;
}

.message-chat-chat-container-a {
  align-items: flex-start;
  text-align: left;
}

.message-chat-chat-container-a__my {
  align-items: flex-end;
  text-align: right;
}

.message-chat__chat-time {
  text-align: left;
}

.message-chat__chat-time__my {
  text-align: right;
}
</style>
