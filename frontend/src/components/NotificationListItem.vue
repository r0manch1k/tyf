<template>
  <div class="notification-list-item bg-secondary p-2">
    <div class="notification-list-item__container d-flex align-items-center">
      <!-- <div class="notification-list-item__icon-container">
        <i class="bi bi-bell text-secondary-xx-light h-100 pb-auto"></i>
      </div> -->
      <div class="notification-list-item__content">
        <div
          class="notification-list-item__text-container d-flex flex-wrap gap-1"
        >
          <p class="notification-list-item__text d-flex align-items-center m-0">
            {{ notification.text }}
          </p>
          <router-link
            v-if="notification.kind === 'post'"
            :to="{
              name: 'post-detail',
              params: { identifier: notification.target },
            }"
            class="notification-list-item__link btn btn-light p-0"
          >
            Подробнее
          </router-link>
          <router-link
            v-if="notification.kind === 'profile'"
            :to="{
              name: 'profile',
              params: { username: notification.target },
            }"
            class="notification-list-item__link btn btn-light p-0"
          >
            Подробнее
          </router-link>
        </div>
        <div
          class="notification-list-item__date d-flex align-items-center gap-2"
        >
          <div
            class="notification-list-item__date-container d-flex align-items-center fs-6 text-secondary-xx-light gap-2"
          >
            {{ notification.created_at }}
          </div>
          <button
            class="btn btn-light text-decoration-none p-0"
            @click="read"
            :disabled="loadingRead || notification.read"
          >
            <span
              v-if="notification.read && !loadingRead"
              class="text-secondary-xx-ligth fw-normal"
              >Прочитано</span
            >
            <span v-else-if="!loadingRead" class="text-primary fw-normal"
              >Отметить прочитанным</span
            >
            <span v-else class="text-primary fw-normal">Отмечаю...</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, defineProps } from "vue";
import { useStore } from "vuex";
import type NotificationModel from "@/models/NotificationModel";

const store = useStore();
const loadingRead = ref<boolean>(false);

const props = defineProps<{
  notification: NotificationModel;
}>();

const read = async () => {
  loadingRead.value = true;

  await store
    .dispatch("notification/readNotification", props.notification.id)
    .finally(() => {
      loadingRead.value = false;
    });
};
</script>

<style scoped>
.notification-list-item {
  border-radius: 0.4rem;
  width: fit-content;
}
</style>
