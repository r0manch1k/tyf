<template>
  <div class="chat" v-if="loading">
    <div class="chat__container">
      <div class="chat__chats">
        <div class="chat__chat">
          <!-- <div class="chat__chat-avatar"></div> -->
          <div class="chat__chat -info">
            <div class="chat__chat -name">{{ chat.name }}</div>
            <div>
              <MessageChat
                v-for="message in chat.messages"
                :key="message.id"
                :message="message"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <LoadingCircle v-else />
</template>

<script lang="ts" setup>
import { ref, defineProps, computed, onMounted } from "vue";
import type { ChatDetailModel } from "@/models/ChatModel";
import { useStore } from "vuex";
import MessageChat from "@/components/MessageChat.vue";
import LoadingCircle from "@/components/LoadingCircle.vue";

const props = defineProps<{
  uuid: string;
}>();

const loading = ref(false);
const store = useStore();
const chat = computed<ChatDetailModel>(() =>
  store.getters["chat/getChatByUUID"](props.uuid)
);

onMounted(async () => {
  loading.value = true;

  await Promise.all([
    store.dispatch("chat/fetchChatByUUID", { uuid: props.uuid }),
  ])
    .then(() => {
      console.log(store.getters["chat/getChatByUUID"](props.uuid));
      connectWebsocket();
    })
    .finally(() => {
      loading.value = false;
    });
});

function connectWebsocket() {
  const websocket = new WebSocket(`ws://localhost:8000/ws/chat/${props.uuid}/`);

  websocket.onmessage = (event) => {
    const messages = JSON.parse(event.data);
    console.log(messages);
  };

  websocket.onopen = () => {
    console.log("Connected to the websocket");
  };

  websocket.onclose = () => {
    console.log("Disconnected from the websocket");
  };
}
</script>
