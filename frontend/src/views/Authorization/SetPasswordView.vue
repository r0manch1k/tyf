<template>
  <div class="set-password container-fluid">
    <div
      class="set-password__wrapper flex row vh-100 align-items-center justify-content-center"
      style="min-height: 100vh"
    >
      <div
        class="set-password__content col-12 row col-sm-8 col-md-6 col-lg-5 col-xl-4"
      >
        <Message
          :message="message"
          :show="showMessage"
          @update:show="showMessage = $event"
        />
        <div
          class="set-password__form bg-secondary rounded p-4"
          style="border-radius: 1rem !important"
        >
          <div
            class="set-password__header text-center align-items-center justify-content-between mb-4"
          >
            <h3 class="set-password__title fs-5">Введите новый пароль</h3>
          </div>
          <form
            method="post"
            role="form"
            v-on:submit.prevent="setPasswordSubmit"
          >
            <div class="set-password__field form-floating mb-2">
              <PasswordField v-model="password1" />
            </div>
            <div class="set-password__field form-floating mb-3">
              <RepeatPasswordField v-model="password2" />
            </div>
            <button
              type="submit"
              class="set-password__submit btn btn-primary py-3 w-100 mb-2"
              :disabled="loading"
            >
              <label v-if="!loading" style="color: var(--dark) !important"
                >Продолжить</label
              >
              <LoadingCircle v-else />
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, computed } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import AuthService from "@/services/AuthService";
import MessageModel from "@/models/MessageModel";

import PasswordField from "@/components/Authorization/Fields/PasswordField.vue";
import RepeatPasswordField from "@/components/Authorization/Fields/RepeatPasswordField.vue";
import LoadingCircle from "@/components/LoadingCircle.vue";
import Message from "@/components/Message.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();

const password1 = ref("");
const password2 = ref("");
const loading = ref(true);

const message = computed<MessageModel>(() => store.state.auth.message);
const showMessage = ref(false);

onMounted(async () => {
  loading.value = true;
  await AuthService.checkPasswordResetAccess(
    Array.isArray(route.params.token)
      ? route.params.token[0]
      : route.params.token,
    Array.isArray(route.params.uid) ? route.params.uid[0] : route.params.uid
  )
    .catch((error) => {
      store.commit("error/setShowErrorPage", error.status);
    })
    .finally(() => {
      loading.value = false;
    });
});

const setPasswordSubmit = async () => {
  loading.value = true;

  await AuthService.setPassword(
    password1.value,
    password2.value,
    Array.isArray(route.params.token)
      ? route.params.token[0]
      : route.params.token ?? "",
    Array.isArray(route.params.uid)
      ? route.params.uid[0]
      : route.params.uid ?? ""
  )
    .then(() => {
      const message: MessageModel = {
        text: "Пароль успешно изменен.",
        type: "success",
      };
      store.commit("auth/setMessage", message);
      showMessage.value = true;
      router.push("/login");
    })
    .catch((error) => {
      if (error.status === 401) {
        const message: MessageModel = {
          text: "Ваша сессия смены пароля истекла. Пройдите процесс смены пароля заново.",
          type: "info",
        };
        store.commit("auth/setMessage", message);
        showMessage.value = true;
        router.push("/login");
      } else {
        const message: MessageModel = {
          text:
            error.data?.message ||
            "Что-то пошло не так, повторите попытку позже.",
          type: "error",
        };
        store.commit("auth/setMessage", message);
        showMessage.value = true;
      }
    })
    .finally(() => {
      loading.value = false;
    });
};
</script>

<style scoped>
.row > * {
  padding: 0;
}
</style>
