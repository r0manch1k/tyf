<template>
  <!-- TODO: Change v-if condition for isHome views -->
  <div v-if="isHome" class="main">
    <Header />
    <Sidebar />
    <div
      :class="[
        'main__content',
        { dimmed: isSuggestionsOpen && isHome },
        'mx-0',
        'pb-3',
        'pt-7',
      ]"
    >
      <NotFoundView v-if="isError" />
      <router-view v-else />
    </div>
    <Footer />
  </div>
  <NotFoundView v-else-if="isError" />
  <LoginView v-else-if="isLogin" />
  <RegisterView v-else-if="isRegister" />
  <ResetPasswordView v-else-if="isResetPassword" />
  <SetPasswordView v-else-if="isSetPassword" />
  <VerificationView v-else-if="isVerification" />
  <BackgroundGraphs />
</template>

<script lang="ts" setup>
import BackgroundGraphs from "@/components/BackgroundGraphs.vue";
import Footer from "@/components/Footer.vue";
import Header from "@/components/Header.vue";
import Sidebar from "@/components/Sidebar.vue";
import NotificationModel from "@/models/NotificationModel";
import AuthService from "@/services/AuthService";
import LoginView from "@/views/Authorization/LoginView.vue";
import RegisterView from "@/views/Authorization/RegisterView.vue";
import ResetPasswordView from "@/views/Authorization/ResetPasswordView.vue";
import SetPasswordView from "@/views/Authorization/SetPasswordView.vue";
import VerificationView from "@/views/Authorization/VerificationView.vue";
import NotFoundView from "@/views/NotFoundView.vue";
import { computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

const route = useRoute();
const store = useStore();

const isSuggestionsOpen = computed(() => {
  return store.getters["search/isSuggestionsOpen"];
});

const isError = computed(() => {
  return store.getters["error/getShowErrorPage"];
});

const isLogin = computed(() => route.name === "login");
const isRegister = computed(() => route.name === "register");
const isResetPassword = computed(() => route.name === "reset-password");
const isSetPassword = computed(() => route.name === "reset-password-confirm");
const isVerification = computed(() => route.name === "verification");
const isHome = computed(
  () =>
    !isLogin.value &&
    !isRegister.value &&
    !isResetPassword.value &&
    !isSetPassword.value &&
    !isVerification.value
);

onMounted(async () => {
  await store.dispatch("profile/fetchProfile");
  connectWebsocket();
});

function connectWebsocket() {
  const websocketUrl =
    process.env.NODE_ENV === "production"
      ? process.env.VUE_APP_WS_API_URL_PROD
      : process.env.VUE_APP_WS_API_URL_DEV;

  const websocket = new WebSocket(
    `${websocketUrl}/notifications/?token=${AuthService.getAccessTokenFromLocalStorage()}`
  );

  websocket.onmessage = (event) => {
    const data: NotificationModel = JSON.parse(event.data);
    store.dispatch("notification/addNotification", data);
  };

  websocket.onopen = async () => {
    console.log("Connected to the notifications websocket");
    await store.dispatch("notification/fetchAllNotifications");
  };

  websocket.onclose = () => {
    console.log("Disconnected from the notifications websocket");

    setTimeout(() => {
      connectWebsocket();
    }, 5000);
  };
}
</script>

<style>
@import "@/assets/styles/css/bootstrap.min.css";
@import "@/assets/styles/css/main.css";

.main {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.dimmed {
  filter: brightness(60%);
}

#app {
  overflow-x: hidden;
  scrollbar-width: none;
  scroll-behavior: smooth;
  overflow-y: auto;
  font-family: "MesloLGS NF", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

#app::-webkit-scrollbar {
  display: none;
}

.main__content {
  background-color: rgba(30, 30, 35, 0.5);
  top: 0 !important;
  flex: 1 !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-start !important;
}

.btn {
  border-radius: 0.4rem !important;
}

.btn-check:focus + .btn,
.btn:focus {
  box-shadow: none;
}

.btn:disabled,
.btn.disabled,
fieldset:disabled .btn {
  opacity: 1;
}
</style>
