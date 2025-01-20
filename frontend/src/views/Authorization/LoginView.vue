<template>
  <div class="login-view container-fluid">
    <div
      class="login-view__flex row vh-100 align-items-center justify-content-center"
      style="min-height: 100vh"
    >
      <div
        class="login-view__col col-12 row col-sm-8 col-md-6 col-lg-5 col-xl-4"
      >
        <Message
          :message="message"
          :show="showMessage"
          @update:show="showMessage = $event"
        />
        <div class="login-view__box bg-dark-light p-4">
          <div
            class="login-view__header text-center align-items-center justify-content-between mb-4"
          >
            <h3
              class="login-view__title fs-5"
              style="color: var(--light) !important"
            >
              Войти в аккаунт
              <router-link to="/">
                <span
                  class="login-view__brand text-primary fs-5"
                  style="color: var(--primary) !important"
                >tyf</span
                >
              </router-link>
            </h3>
          </div>
          <OAuthButtons />
          <div class="login-view__divider col-md-12 mb-3">
            <div class="login-or">
              <hr class="hr-or" />
              <span class="span-or small" style="user-select: none">ИЛИ</span>
            </div>
          </div>
          <form method="post" role="form" @submit.prevent="loginSubmit">
            <div class="login-view__email form-floating mb-2">
              <EmailField v-model="email" />
            </div>
            <div class="login-view__password form-floating mb-3">
              <PasswordField v-model="password" />
            </div>
            <router-link to="/login/reset-password">
              <div
                class="login-view__forgot d-flex align-items-center justify-content-between mb-3"
              >
                <a>Забыли пароль?</a>
              </div>
            </router-link>
            <button
              type="submit"
              class="login-view__submit btn btn-primary py-3 w-100 mb-4"
              :disabled="loading"
            >
              <label v-if="!loading" style="color: var(--dark) !important"
              >Войти</label
              >
              <LoadingCircle v-else class="spinner-border-sm" />
            </button>
          </form>
          <p class="login-view__register text-center mb-0">
            У вас нет аккаунта?
            <router-link to="/register"><a>Зарегистрироваться.</a></router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import MessageModel from "@/models/MessageModel";
import AuthService from "@/services/AuthService";
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import EmailField from "@/components/Authorization/Fields/EmailField.vue";
import PasswordField from "@/components/Authorization/Fields/PasswordField.vue";
import OAuthButtons from "@/components/Authorization/OAuthButtons.vue";
import LoadingCircle from "@/components/LoadingCircle.vue";
import Message from "@/components/Message.vue";

const store = useStore();
const router = useRouter();

const email = ref("");
const password = ref("");
const loading = ref(false);

const message = computed<MessageModel>(() => store.state.auth.message);
const showMessage = ref(false);

const loginSubmit = async () => {
  loading.value = true;
  showMessage.value = false;
  AuthService.login(email.value, password.value)
    .then(() => {
      store.dispatch("profile/fetchProfile");
      router.push("/");
    })
    .catch((error) => {
      const message: MessageModel = {
        text: error.data.detail || error.data.message,
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
.login-view__box,
.login-view__submit {
  border-radius: 0.4rem;
}

.login-or {
  position: relative;
  color: #aaa;
  margin-top: 10px;
  margin-bottom: 10px;
  padding-top: 10px;
  padding-bottom: 10px;
}

.span-or {
  display: block;
  position: absolute;
  left: 50%;
  top: -2px;
  margin-left: -25px;
  background-color: var(--dark-light);
  width: 50px;
  text-align: center;
}

.hr-or {
  height: 1px;
  margin-top: 0px !important;
  margin-bottom: 0px !important;
}

.row > * {
  padding: 0;
}
</style>
