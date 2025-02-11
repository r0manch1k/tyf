<template>
  <div
    class="notification-list-item ps-2"
    :style="{
      borderLeft: notification.read
        ? '2px solid var(--secondary-light)'
        : '2px solid var(--primary)',
    }"
  >
    <div class="notification-list-item__container d-flex align-items-center">
      <div class="notification-list-item__content">
        <h2
          class="fs-6 text-start m-0"
          :class="{
            'text-secondary-xx-light': notification.read,
            'text-primary': !notification.read,
          }"
        >
          <span v-if="notification.kind === 'post'">Новый пост</span>
          <span v-if="notification.kind === 'follower'">Новый подписчик</span>
          <span v-if="notification.kind === 'message'">Новое сообщение</span>
          <span v-if="notification.kind === 'chat'">Новый чат</span>
        </h2>

        <div
          class="notification-list-item__text-container d-flex flex-wrap gap-1"
        >
          <p
            class="notification-list-item__text d-flex align-items-center m-0"
            :class="{
              'text-secondary-light': notification.read,
              'text-light': !notification.read,
            }"
          >
            {{ notification.text }}
          </p>
          <router-link
            v-if="notification.kind === 'post'"
            :to="{
              name: 'post-detail',
              params: { identifier: notification.target },
            }"
            class="notification-list-item__link btn-light text-decoration-underline p-0"
            :class="{
              'text-secondary-light': notification.read,
              'text-light': !notification.read,
            }"
          >
            Подробнее
          </router-link>
          <router-link
            v-if="notification.kind === 'follower'"
            :to="{
              name: 'profile',
              params: { username: notification.target },
            }"
            class="notification-list-item__link btn-light text-decoration-underline p-0"
            :class="{
              'text-secondary-light': notification.read,
              'text-light': !notification.read,
            }"
          >
            Подробнее
          </router-link>
          <router-link
            v-if="notification.kind === 'message'"
            :to="{
              name: 'chat',
              params: { uuid: notification.target },
            }"
            class="notification-list-item__link btn-light text-decoration-underline p-0"
            :class="{
              'text-secondary-light': notification.read,
              'text-light': !notification.read,
            }"
          >
            Подробнее
          </router-link>
          <router-link
            v-if="notification.kind === 'chat'"
            :to="{
              name: 'chat',
              params: { uuid: notification.target },
            }"
            class="notification-list-item__link btn-light text-decoration-underline p-0"
            :class="{
              'text-secondary-light': notification.read,
              'text-light': !notification.read,
            }"
          >
            Подробнее
          </router-link>
        </div>
        <div
          class="notification-list-item__date d-flex align-items-center gap-2"
        >
          <div
            class="notification-list-item__date-container d-flex align-items-center fs-6 gap-2"
            :class="{
              'text-secondary-x-light': notification.read,
              'text-secondary-xx-light': !notification.read,
            }"
          >
            {{ created_at }}
          </div>
          <button
            class="btn btn-light text-decoration-none p-0"
            @click="read"
            :disabled="loadingRead || notification.read"
            v-if="!notification.read"
          >
            <span class="text-primary fw-normal" v-if="!loadingRead"
              >Отметить прочитанным</span
            >
            <span v-else>Отмечаю...</span>
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
import moment from "moment";
import "moment/locale/ru";

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

const created_at = moment(props.notification.created_at).fromNow();
</script>

<style scoped>
.notification-list-item {
  width: fit-content;
}
</style>
