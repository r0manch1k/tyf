<template>
  <div class="chats-view px-5 h-100">
    <div class="chats-view__container container-fluid p-0">
      <div class="chat-list row" v-if="!loading">
        <div class="chat-list__sidebar col-md-3">
          <h1 class="chats-view__title fs-5 fw-normal text-start m-0">Чаты</h1>
          <p
            class="chats-view__subtitle fs-6 text-secondary-xx-light text-start m-0"
          >
            Ваши чаты
          </p>
          <hr class="my-1" />
          <SearchBarChat class="mb-1" />
          <ul
            class="chat-list__list list-group list-group-flush mt-2"
            v-if="!loadingChats"
          >
            <ChatListItem
              v-for="chat in Object.values(chats)"
              :key="chat.id"
              :chat="chat"
              :selected="chat.uuid === uuid"
            />
          </ul>
          <LoadingCircle v-else class="spinner-border-sm mx-auto my-auto" />
        </div>
        <div class="chat-window col-md-9" v-if="uuid">
          <Chat :uuid="uuid" class="flex-grow-1 mt-2" />
        </div>
      </div>
      <LoadingCircle v-else class="spinner-border-sm mx-auto my-auto" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, defineProps } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import type { ProfileListItemModel } from "@/models/ProfileModel";
import type { ChatListItemModel } from "@/models/ChatModel";
import ChatListItem from "@/components/ChatListItem.vue";
import SearchBarChat from "@/components/SearchBarChat.vue";
import Chat from "@/components/Chat.vue";
import LoadingCircle from "@/components/LoadingCircle.vue";

const props = defineProps<{
  uuid?: string;
}>();

const store = useStore();
const route = useRoute();
const loading = ref(false);
const loadingChats = ref(false);
const chats = computed<Record<string, ChatListItemModel>>(
  () => store.state.chat.chats
);
const profile = computed<ProfileListItemModel>(
  () => store.state.profile.profile
);

onMounted(async () => {
  loadingChats.value = true;

  await store.dispatch("profile/fetchProfile");

  await Promise.all([
    store.dispatch("chat/fetchProfileChats", profile.value.username),
  ]).finally(() => {
    loadingChats.value = false;
  });
});
</script>

<style scoped>
.chats-view__title {
  color: var(--primary);
}

.chat-list__sidebar {
  overflow-y: auto;
}
</style>
