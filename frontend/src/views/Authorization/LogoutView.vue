<template>
  <LoadingCircle v-if="loading" />
</template>

<script lang="ts" setup>
import type MessageModel from "@/models/MessageModel";
import AuthService from "@/services/AuthService";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import LoadingCircle from "@/components/LoadingCircle.vue";

const store = useStore();
const router = useRouter();

const loading = ref(false);

const logoutSubmit = async () => {
  loading.value = true;
  AuthService.logout()
    .then(() => {
      router.push("/login");
    })
    .catch((error) => {
      const message: MessageModel = {
        text: error.data.message,
        type: "error",
      };
      store.dispatch("auth/setMessage", message);
    })
    .finally(() => {
      loading.value = false;
    });
};

onMounted(() => {
  logoutSubmit();
});
</script>
