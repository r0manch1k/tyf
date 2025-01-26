<template>
  <div class="notifications px-5" v-if="!loading">
    <div class="notifications__container container-fluid p-0">
      <div class="notifications__row row">
        <div class="notifications__main col-md-9 d-flex flex-column gap-2">
          <div
            class="notifications__header d-flex justify-content-between alight-items-center bg-dark-light p-2"
          >
            <div>
              <h1 class="notifications__title fs-5 fw-normal text-start m-0">
                Ваши уведомления
              </h1>
              <p
                class="notifications__subtitle fs-6 text-secondary-xx-light text-start m-0"
              >
                После прочтения сообщения будут удалены навсегда
              </p>
            </div>
            <div
              class="notifications__header-actions d-flex alight-items-center px-1"
              v-if="notifications.length > 0"
            >
              <button
                class="btn btn-light p-0"
                @click="readAll"
                :disabled="loadingReadAll"
              >
                <span v-if="loadingReadAll">Отмечаю...</span>
                <span v-else>Отметить все как прочитанные</span>
              </button>
            </div>
          </div>
          <div
            class="notifications__list d-flex flex-column alight-items-start gap-2"
          >
            <NotificationListItem
              v-for="notification in notificationsSorted"
              :key="notification.id"
              :notification="notification"
            />
          </div>
        </div>
        <div class="notifications__sidebar col-md-3 pt-3 bg-dark-light"></div>
      </div>
    </div>
  </div>
  <LoadingCircle v-else />
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

onMounted(async () => {
  loading.value = true;
  await store.dispatch("notification/fetchUnreadNotifications").finally(() => {
    loading.value = false;
  });
});

const readAll = async () => {
  loadingReadAll.value = true;
  await store.dispatch("notification/readAllNotifications").finally(() => {
    loadingReadAll.value = false;
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
  color: var(--light);
  text-decoration: underline;
  text-decoration-color: var(--primary);
}
</style>
