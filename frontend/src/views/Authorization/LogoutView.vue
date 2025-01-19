<template>
  <LoadingCircle v-if="isLoading" />
</template>

<script lang="ts" setup>
import LoadingCircle from "@/components/LoadingCircle.vue";
import api from "@/stores/services/api";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const isLoading = ref(false);
const router = useRouter();

const logoutSubmit = async () => {
  isLoading.value = true;
  const refreshToken = localStorage.getItem("refreshToken") ?? "";

  if (refreshToken) {
    await api
      .post("users/logout/", {
        token: { refresh: refreshToken },
      })
      .then((response) => {
        console.log(response);
        if (response.status == 200) {
          localStorage.removeItem("accessToken");
          localStorage.removeItem("refreshToken");
        }
      })
      .catch((error) => console.error(error));
  }
  router.push("login/");
};

onMounted(() => {
  logoutSubmit();
});
</script>
