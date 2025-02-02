<template>
  <div class="notifications px-5">
    <div class="notifications__container container-fluid p-0">
      <h1 class="notifications__title fs-5 fw-normal text-start m-0">
        Уведомления
      </h1>
      <p
        class="notifications__subtitle fs-6 text-secondary-xx-light text-start m-0"
      >
        Здесь вы можете увидеть все ваши уведомления
      </p>

      <hr class="my-1" />
      <div
        class="notifications__header d-flex flex-row gap-3 justify-content-start"
        v-if="!loading"
      >
        <button
          class="btn btn-light text-decoration-underline p-0 mb-2"
          @click="readAll"
          v-if="notificationsUnreadCount > 0"
          :disabled="loadingReadAll"
        >
          <span v-if="loadingReadAll">Отмечаю...</span>
          <span v-else>Отметить все как прочитанные</span>
        </button>
        <button
          class="btn btn-light text-decoration-underline p-0 mb-2"
          @click="deleteRead"
          v-if="notifications.length - notificationsUnreadCount > 0"
          :disabled="loadingDeleteRead"
        >
          <span v-if="loadingDeleteRead">Удаляю...</span>
          <span v-else>Удалить прочитанные</span>
        </button>
      </div>

      <div class="notifications__row row" v-if="!loading">
        <div class="notifications__main col-md-9 d-flex flex-column gap-2">
          <div
            class="notifications__list d-flex flex-column alight-items-start gap-2 mt-2"
          >
            <NotificationListItem
              v-for="notification in notificationsSorted"
              :key="notification.id"
              :notification="notification"
            />
          </div>
        </div>
        <!-- <div class="notifications__sidebar col-md-3 pt-3 bg-dark-light"></div> -->
      </div>
      <LoadingCircle class="spinner-border-sm mx-auto my-auto" v-else />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";
import type NotificationModel from "@/models/NotificationModel";
import NotificationListItem from "@/components/NotificationListItem.vue";
import LoadingCircle from "@/components/LoadingCircle.vue";

const store = useStore();
const loading = ref<boolean>(false);
const loadingReadAll = ref<boolean>(false);
const loadingDeleteRead = ref<boolean>(false);

const notifications = computed<NotificationModel[]>(
  () => store.state.notification.notifications
);

const notificationsSorted = computed<NotificationModel[]>(() => {
  return notifications.value.slice().sort((a, b) => {
    if (a.read === b.read) {
      return (
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
    }
    return a.read ? 1 : -1;
  });
});

const notificationsUnreadCount = computed(() => {
  return notifications.value.filter((notification) => !notification.read)
    .length;
});

onMounted(async () => {
  loading.value = true;
  await store.dispatch("notification/fetchAllNotifications").finally(() => {
    loading.value = false;
  });
});

const readAll = async () => {
  loadingReadAll.value = true;
  await store.dispatch("notification/readAllNotifications").finally(() => {
    loadingReadAll.value = false;
  });
};

const deleteRead = async () => {
  loadingDeleteRead.value = true;
  await store.dispatch("notification/deleteReadNotifications").finally(() => {
    loadingDeleteRead.value = false;
  });
};
</script>

<style scoped>
.notifications__header,
.notifications__list,
.notifications__sidebar {
  border-radius: 0.4rem;
}

.notifications__title {
  color: var(--primary);
}
</style>
