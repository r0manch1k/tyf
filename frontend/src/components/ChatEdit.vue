<template>
  <div class="chat-edit">
    <div class="chat-edit__header bg-dark-light p-3">
      <div class="chat-edit__header-title fs-6 text-secondary-xx-light">
        <button class="btn btn-light fs-6" @click="backToChat">
          Назад к чату
        </button>
      </div>
      <div class="chat-edit__header-actions"></div>
    </div>
    <div class="chat-edit__body bg-dark-x-light p-3">
      <form enctype="multipart/form-data" @submit.prevent="updateChat">
        <div class="mb-3">
          <label for="chatName" class="form-label fs-6 text-secondary-xx-light"
            >Название чата</label
          >
          <input
            type="text"
            class="form-control bg-dark-x-light text-secondary-xx-light fs-7"
            id="chatName"
            v-model="chatEdit.name"
          />
        </div>

        <div class="form-group mb-3">
          <label
            for="chatThumbnail"
            class="chat-edit__field-label form-label fs-6 text-secondary-xx-light"
            >Аватар чата</label
          >
          <input
            type="file"
            class="form-control bg-dark-x-light text-secondary-xx-light fs-7"
            id="chatThumbnail"
            @change="
              thumbnail = ($event.target as HTMLInputElement).files?.[0] || null
            "
          />
        </div>
        <div class="d-flex align-items-center gap-2">
          <button
            type="submit"
            class="btn btn-submit text-decoration-none"
            :class="{
              'action-checked': canSave,
              'action-unchecked': !canSave,
            }"
            :disabled="!canSave || loadingUpdate"
          >
            <span v-if="!loadingUpdate"> Сохранить </span>
            <LoadingCircle v-else class="spinner-border-sm" />
          </button>
          <p class="text-alert fs-7 m-0">{{ errorMessage }}</p>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts" setup>
import _ from "lodash";
import { ref, computed, defineProps } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import type { ChatDetailModel } from "@/models/ChatModel";
import ChatDataService from "@/services/ChatDataService";

const props = defineProps<{
  uuid: string;
}>();

const store = useStore();
const route = useRoute();
const router = useRouter();
const loadingUpdate = ref(false);

const chat = ref<ChatDetailModel>({
  ...store.getters["chat/getChatByUUID"](props.uuid),
});

const chatEdit = ref<ChatDetailModel>({
  ...chat.value,
});
const thumbnail = ref<File | null>(null);
const errorMessage = ref("");

const canSave = computed(() => {
  return !_.isEqual(chat.value, chatEdit.value);
});

function isError() {
  return errorMessage.value !== "";
}

function clearError() {
  errorMessage.value = "";
}

const updateChat = async () => {
  loadingUpdate.value = true;

  clearError();

  const chatEditData = { ...chatEdit.value };
  delete chatEditData.thumbnail;

  await Promise.all([
    thumbnail.value
      ? ChatDataService.updateThumbnail(chat.value.uuid, thumbnail.value)
      : Promise.resolve(),
    ChatDataService.updateChat(chatEditData),
  ]).catch((error) => {
    console.error(error);
    if (error.data && typeof error.data === "object") {
      for (const key in error.data) {
        if (Object.prototype.hasOwnProperty.call(error.data, key)) {
          errorMessage.value = `${error.data[key].join(", ")}`;
          break;
        }
      }
    } else {
      errorMessage.value = error.data;
    }
  });
};

const backToChat = () => {
  router.push({ name: "chat", params: { uuid: route.params.uuid } });
};
</script>

<style scoped>
.chat-edit,
.chat-edit__header {
  border-radius: 0.4rem;
}

.chat-edit__field-label {
  text-align: left;
  font-size: 1rem;
  text-decoration: underline;
  text-decoration-color: var(--primary);
}

.form-control {
  background-color: var(--secondary);
  color: var(--light);
  padding: 0.2rem 0.25rem;
  border: 0;
  border-radius: 0.4rem;
}

.form-control:focus,
.form-control:active {
  background-color: var(--secondary);
  color: var(--light);
  box-shadow: 0 0 0 0.25rem var(--primary);
}

.form-control:disabled,
.form-control:read-only {
  background-color: var(--secondary);
}

input[type="date" i]::-webkit-inner-spin-button,
input[type="date" i]::-webkit-calendar-picker-indicator {
  filter: invert(1);
  border-radius: 5px;
}
</style>
