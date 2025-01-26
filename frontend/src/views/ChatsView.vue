<template>
  <div class="chats-view" v-if="!loading">
    <div class="chat-list">
      <ul>
        <ChatListItem
          v-for="chat in chats"
          :key="chat.id"
          :chat="chat"
          @click="selectChat(chat)"
        />
      </ul>
    </div>
    <div class="chat-window" v-if="selectedChat">
      <Chat :uuid="selectedChat.uuid" />
    </div>
  </div>
  <LoadingCircle v-else />
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";
import type { ProfileListItemModel } from "@/models/ProfileModel";
import type { ChatListItemModel } from "@/models/ChatModel";
import ChatListItem from "@/components/ChatListItem.vue";
import Chat from "@/components/Chat.vue";
import LoadingCircle from "@/components/LoadingCircle.vue";

const loading = ref(false);
const chats = ref<ChatListItemModel[]>([]);
const selectedChat = ref<ChatListItemModel | null>(null);

const store = useStore();
const profile = computed<ProfileListItemModel>(
  () => store.getters["profile/getProfile"]
);

onMounted(async () => {
  loading.value = true;

  await store.dispatch("profile/fetchProfile");

  await Promise.all([
    store.dispatch("chat/fetchProfileChats", profile.value.username),
  ])
    .then(() => {
      chats.value = store.getters["chat/getChats"];
    })
    .finally(() => {
      loading.value = false;
    });
});

const selectChat = (chat: ChatListItemModel) => {
  selectedChat.value = chat;
};
</script>
