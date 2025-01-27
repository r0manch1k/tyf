<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    style="display: none"
    width="16"
    height="16"
    fill="currentColor"
    class="bi bi-arrow-left-short"
    viewBox="0 0 16 16"
  >
    <symbol id="arrow-left" fill="currentColor" viewBox="0 0 16 16">
      <path
        fill-rule="evenodd"
        d="M12 8a.5.5 0 0 1-.5.5H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H11.5a.5.5 0 0 1 .5.5"
      />
    </symbol>
  </svg>
  <div :class="{ 'd-none': loading }">
    <div class="container-fluid">
      <div
        class="reset-password-view__wrapper flex row vh-100 align-items-center justify-content-center"
        style="min-height: 100vh"
      >
        <div
          class="reset-password-view__content col-12 row col-sm-8 col-md-6 col-lg-5 col-xl-4"
        >
          <Message
            :message="message"
            :show="showMessage"
            @update:show="showMessage = $event"
          />
          <div
            class="reset-password-view__form-container bg-secondary rounded p-4"
            style="border-radius: 1rem !important"
          >
            <div class="reset-password-view__header py-3 mb-4">
              <div class="position-relative">
                <div
                  class="reset-password-view__back-button position-absolute top-50 start-0 translate-middle-y"
                >
                  <router-link to="/login">
                    <a class="float-start">
                      <svg width="35" height="35" role="img">
                        <use xlink:href="#arrow-left" />
                      </svg>
                    </a>
                  </router-link>
                </div>
                <div
                  id="reset-password-title"
                  class="reset-password-view__title position-absolute top-50 start-50 translate-middle"
                  style="width: 60% !important"
                >
                  <h3 class="text-center fs-5" style="margin: 0 !important">
                    Восстановление пароля
                  </h3>
                </div>
              </div>
            </div>
            <form
              method="post"
              role="form"
              v-on:submit.prevent="resetPasswordSubmit"
            >
              <div class="form-floating mb-3">
                <EmailField v-model="email" />
              </div>
              <button
                type="submit"
                class="reset-password-view__submit-button btn btn-primary py-3 w-100 mb-4"
              >
                <label style="color: var(--dark) !important">Продолжить</label>
              </button>
            </form>
            <router-link to="/register">
              <p class="reset-password-view__register-link text-center mb-0">
                <a>Создать новый аккаунт</a>
              </p>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
  <LoadingCircle class="mx-auto my-auto" v-if="loading" />
</template>

<script lang="ts" setup>
import MessageModel from "@/models/MessageModel";
import AuthService from "@/services/AuthService";
import { computed, ref } from "vue";
import { useStore } from "vuex";

import EmailField from "@/components/Authorization/Fields/EmailField.vue";
import LoadingCircle from "@/components/LoadingCircle.vue";
import Message from "@/components/Message.vue";

const store = useStore();

const email = ref("");
const loading = ref(false);

const message = computed<MessageModel>(() => store.state.auth.message);
const showMessage = ref(false);

const resetPasswordSubmit = async () => {
  loading.value = true;
  showMessage.value = false;
  await AuthService.resetPassword(email.value)
    .then(() => {
      console.log("Success");
    })
    .catch((error) => {
      const message: MessageModel = {
        text: error.data.message,
        type: "error",
      };
      store.dispatch("auth/setMessage", message);
      showMessage.value = true;
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
