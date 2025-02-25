<template>
  <Message
    :message="message"
    :show="showMessage"
    @update:show="showMessage = $event"
  />
  <LoadingCircle class="mx-auto my-auto" v-if="loading" />
  <NotFoundView v-else />
</template>

<script lang="ts" setup>
import type MessageModel from "@/models/MessageModel";
import AuthService from "@/services/AuthService";
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import LoadingCircle from "@/components/LoadingCircle.vue";
import Message from "@/components/Message.vue";
import NotFoundView from "@/views/NotFoundView.vue";

const store = useStore();
const router = useRouter();

const loading = ref(true);

const message = computed<MessageModel>(() => store.state.auth.message);
const showMessage = ref(false);

const handleYandexRedirect = async () => {
  const hash = window.location.hash;

  if (hash) {
    if (hash.split("&")[0].split("=")[0] == "#access_token") {
      const token = hash.split("&")[0].split("=")[1];

      await AuthService.handleOAuthRedirect(token, "yandex")
        .then(() => {
          router.push("/");
        })
        .catch((error) => {
          const message: MessageModel = {
            text: error.data.message,
            type: "error",
          };
          store.commit("auth/setMessage", message);
          showMessage.value = true;
          router.push("/login");
        })
        .finally(() => {
          loading.value = false;
        });
    } else {
      loading.value = false;
    }
  }
};

onMounted(() => {
  handleYandexRedirect();
});
</script>
