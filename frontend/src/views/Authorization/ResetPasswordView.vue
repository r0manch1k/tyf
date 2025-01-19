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
  <div :class="{ 'container-fluid': true, 'd-none': loading }">
    <div
      class="flex row vh-100 align-items-center justify-content-center"
      style="min-height: 100vh"
    >
      <div class="col-12 row col-sm-8 col-md-6 col-lg-5 col-xl-4">
        <Messages ref="messagesComponent" />
        <div
          class="bg-secondary rounded p-4"
          style="border-radius: 1rem !important"
        >
          <div class="py-3 mb-4">
            <div class="position-relative">
              <div class="position-absolute top-50 start-0 translate-middle-y">
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
                class="position-absolute top-50 start-50 translate-middle"
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
              class="btn btn-primary py-3 w-100 mb-4"
              style="border-radius: 1rem !important"
            >
              <label style="color: var(--dark) !important">Продолжить</label>
            </button>
          </form>
          <router-link to="/register">
            <p class="text-center mb-0">
              <a>Создать новый аккаунт</a>
            </p>
          </router-link>
        </div>
      </div>
    </div>
  </div>
  <LoadingCircle v-if="loading" />
</template>

<script lang="ts" setup>
import api from "@/stores/services/api";
import { ref } from "vue";
import { useRouter } from "vue-router";

import EmailField from "@/components/Authorization/Fields/EmailField.vue";
import Messages from "@/components/Authorization/Messages.vue";
import LoadingCircle from "@/components/LoadingCircle.vue";

interface MessagesComponent {
  addMessage: (message: { type: string; text: string }) => void;
}

const router = useRouter();

const email = ref("");
const loading = ref(false);
const messagesComponent = ref<MessagesComponent | null>(null);

const resetPasswordSubmit = async () => {
  loading.value = true;
  console.log(email.value);

  await api
    .post("users/reset_password/", {
      email: email.value,
    })
    .then((response) => {
      loading.value = false;
      if (response.status === 201) {
        console.log(response.data.payload.uid, response.data.payload.token);
        router.push(
          `/verify/${response.data.payload.uid}/${response.data.payload.token}`
        );
      } else {
        const errorMessage =
          response?.data?.message ||
          "Что-то пошло не так, повторите попытку позже.";
        if (messagesComponent.value) {
          messagesComponent.value.addMessage({
            type: "error",
            text: errorMessage,
          });
        }
      }
    })
    .catch((error) => {
      console.log(error);
      loading.value = false;
      if (messagesComponent.value) {
        messagesComponent.value.addMessage({
          type: "error",
          text: "Что-то пошло не так, повторите попытку позже.",
        });
      }
    });
};
</script>

<style scoped></style>
