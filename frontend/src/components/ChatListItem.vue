<template>
  <router-link
    class="chat-list-item py-1 px-2 fs-6"
    :class="{ 'chat-list-item__selected': selected }"
    :to="{ name: 'chat', params: { uuid: chat.uuid } }"
  >
    <div class="chat-list-item__container">
      <div class="chat-list-item__chat d-flex align-items-center gap-2">
        <div class="chat-list-item__chat-avatar">
          <img
            class="chat-list-item__chat-avatar-img rounded-circle"
            style="width: 50px; height: 50px"
            :src="chat.thumbnail"
          />
        </div>
        <div
          class="chat-list-item__chat-info d-flex flex-column text-start w-100"
        >
          <div
            class="chat-list-item_header d-flex align-items-center justify-content-between align-items-center"
          >
            <div
              class="chat-list-item__chat-name fw-bold"
              :class="{ 'chat-list-item__chat-name__selected': selected }"
            >
              {{
                chat.name.length > 20
                  ? chat.name.substring(0, 20) + "..."
                  : chat.name
              }}
            </div>
            <div
              class="chat-list-item__updated_at fs-7"
              :class="{ 'chat-list-item__updated_at__selected': selected }"
            >
              {{ updated_at }}
            </div>
          </div>

          <div
            class="chat-list-item__chat-last-message fs-7"
            :class="{ 'chat-list-item__chat-last-message__selected': selected }"
          >
            {{
              chat.last_message.text.length > 25
                ? chat.last_message.text.substring(0, 25) + "..."
                : chat.last_message.text
            }}
          </div>
        </div>
      </div>
    </div>
  </router-link>
</template>

<script lang="ts" setup>
import { ref, defineProps, computed } from "vue";
import type { ChatListItemModel } from "@/models/ChatModel";
import moment from "moment";
import "moment/locale/ru";

const props = defineProps<{
  chat: ChatListItemModel;
  selected: boolean;
}>();

const chat = ref<ChatListItemModel>(props.chat);

const updated_at = computed(() => {
  const now = moment();
  const messageTime = moment(chat.value.updated_at);

  if (now.isSame(messageTime, "day")) {
    return messageTime.format("HH:mm");
  } else if (now.isSame(messageTime, "week")) {
    return messageTime.format("dddd");
  } else {
    return messageTime.format("DD.MM.YYYY");
  }
});
</script>

<style scoped>
.chat-list-item {
  border-left: 2px solid var(--secondary-light);
  cursor: pointer;
}

.chat-list-item__selected {
  border-left: 2px solid var(--primary);
}

.chat-list-item__chat-name {
  color: var(--secondary-xx-light);
}

.chat-list-item__chat-name__selected {
  color: var(--primary);
}

.chat-list-item__updated_at {
  color: var(--secondary-light);
}

.chat-list-item__updated_at__selected {
  color: var(--secondary-x-light);
}

.chat-list-item_header {
  height: 1.25rem;
}

.chat-list-item__chat-last-message {
  height: 1.5rem;
  color: var(--secondary-light);
}

.chat-list-item__chat-last-message__selected {
  color: var(--secondary-xx-light);
}
</style>
