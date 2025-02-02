<template>
  <div class="chat" v-if="!loading">
    <div class="chat__container d-flex flex-column h-100">
      <div class="chat__chat flex-grow-1 d-flex flex-column h-100">
        <div
          class="chat__chat-header bg-dark-light p-2 d-flex justify-content-between align-items-center"
        >
          <div class="d-flex align-items-center gap-2">
            <img
              :src="chat.thumbnail"
              alt="thumbnail"
              class="chat__chat-avatar-img rounded-circle"
              style="width: 40px; height: 40px"
            />
            <div class="chat__chat-meta d-flex flex-column text-start">
              <div class="chat__chat-name text-primary fs-7">
                {{ chat.name }}
              </div>
              <div
                class="chat-list-item__chat-participants text-secondary-xx-light fs-8"
              >
                {{ participantsUsernames }}
              </div>
            </div>
          </div>
          <div class="chat__chat-actions d-flex gap-2">
            <div class="dropdown">
              <button
                class="btn btn-light navbar-brand dropdown-toggle fs-7 text-secondary-xx-light"
                type="button"
                id="dropdownMenuButton"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                •••
              </button>
              <ul
                class="dropdown-menu dropdown-menu-dark dropdown-menu-end bg-secondary border-0 rounded fs-6 mt-3"
                aria-labelledby="dropdownMenuButton"
              >
                <li>
                  <button class="change-chat-name dropdown-item">
                    Изменить название
                  </button>
                </li>
                <li>
                  <button class="add-participant dropdown-item">
                    Добавить участника
                  </button>
                </li>
                <li>
                  <button class="change-thumbnail dropdown-item">
                    Изменить изображение
                  </button>
                </li>
                <li>
                  <button class="leave-chat dropdown-item">Покинуть чат</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div
          class="chat__chat-info bg-dark-light flex-grow-1 overflow-auto p-3"
          ref="messagesContainer"
        >
          <div class="chat__chat-messages d-flex flex-column gap-2">
            <MessageChat
              v-for="message in sortedMessages"
              :key="message.id"
              :message="message"
            />
          </div>
        </div>
        <div class="chat__chat-input bg-dark-x-light p-2">
          <form class="d-flex gap-2">
            <textarea
              class="form-control bg-dark-x-light text-secondary-xx-light fs-7"
              placeholder="Введите сообщение..."
              v-model="message.text"
            ></textarea>
            <button
              type="submit"
              class="btn btn-submit my-auto fs-7"
              @click.prevent="sendMessage"
              :disabled="loadingSendMesssage || !message.text"
            >
              <span v-if="!loadingSendMesssage">Отправить</span>
              <LoadingCircle v-else class="spinner-border-sm" />
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
  <LoadingCircle v-else class="spinner-border-sm" />
</template>

<script lang="ts" setup>
import {
  ref,
  defineProps,
  computed,
  onMounted,
  onUnmounted,
  watch,
  nextTick,
} from "vue";
import { useStore } from "vuex";
import type { ChatDetailModel } from "@/models/ChatModel";
import type { MessageChatPayloadModel } from "@/models/MessageChatModel";
import type MessageChatModel from "@/models/MessageChatModel";
import ChatDataService from "@/services/ChatDataService";
import MessageChat from "@/components/MessageChat.vue";
import LoadingCircle from "@/components/LoadingCircle.vue";

const props = defineProps<{
  uuid: string;
}>();

let websocket: WebSocket;
const loading = ref(false);
const loadingSendMesssage = ref(false);
const store = useStore();
const chat = computed<ChatDetailModel>(() =>
  store.getters["chat/getChatByUUID"](props.uuid)
);
const sortedMessages = computed<MessageChatModel[]>(() =>
  chat.value && chat.value.messages
    ? [...chat.value.messages].sort(
        (a: MessageChatModel, b: MessageChatModel): number =>
          new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
      )
    : []
);
const participantsUsernames = computed<string>(() =>
  chat.value.participants.map((participant) => participant.username).join(", ")
);
const message = ref<MessageChatPayloadModel>(
  store.getters["chat/getDefaultMessage"]
);

const messagesContainer = ref<HTMLDivElement | null>(null);

async function fetchChat() {
  loading.value = true;

  await Promise.all([store.dispatch("chat/fetchChatByUUID", props.uuid)]).then(
    () => {
      connectWebsocket();
    }
  );
}

onMounted(async () => {
  await fetchChat();
});

function connectWebsocket() {
  websocket = new WebSocket(`ws://localhost:8000/ws/chats/${props.uuid}/`);

  websocket.onmessage = (event) => {
    const message: MessageChatModel = JSON.parse(event.data);
    store.dispatch("chat/addMessage", {
      uuid: props.uuid,
      message: message,
    });
  };

  websocket.onopen = () => {
    console.log("Connected to the chat websocket");
    loading.value = false;
  };

  websocket.onclose = () => {
    console.log("Disconnected from the chat websocket");
    loading.value = true;
    setTimeout(() => {
      connectWebsocket();
    }, 1000);
  };
}

onUnmounted(() => {
  if (websocket) websocket.close();
});

async function sendMessage() {
  const payload: MessageChatPayloadModel = {
    text: message.value.text,
  };

  loadingSendMesssage.value = true;
  await ChatDataService.sendMessage(props.uuid, payload).finally(() => {
    loadingSendMesssage.value = false;
    message.value.text = "";
  });
}

watch(sortedMessages, () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
});

watch(
  () => props.uuid,
  async () => {
    await fetchChat();
  }
);
</script>

<style scoped>
.chat {
  border-radius: 0.4rem;
  height: 78vh;
}

.chat__chat-header {
  flex-shrink: 0;
  border-top-left-radius: 0.4rem;
  border-top-right-radius: 0.4rem;
  border-bottom: 1px solid var(--dark-x-light);
}

.chat__chat-input {
  border-bottom-left-radius: 0.4rem;
  border-bottom-right-radius: 0.4rem;
}

.form-control {
  border: 0;
  border-radius: 0;
  max-height: calc(1.5em + 0.75rem + 2px);
  background-color: var(--dark-x-light);
}

textarea {
  resize: none;
}

.form-control:focus {
  background-color: var(--dark-x-light);
  border: 0;
  box-shadow: none;
  outline: none;
}

.chat__chat-name {
  height: 1.25rem;
}

.chat__chat-participants {
  height: 1.5rem;
}

.btn-submit {
  min-width: 6rem;
}

.dropdown-toggle::after {
  display: none;
  margin: 0;
  border: 0;
}
</style>
