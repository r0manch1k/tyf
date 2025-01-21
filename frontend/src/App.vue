<template>
  <!-- TODO: Change v-if condition for isHome views -->
  <div v-if="isHome" class="main">
    <Header />
    <Sidebar />
    <div class="main__content bg-dark-light mx-0 pb-3 pt-7">
      <NotFoundView v-if="isError" />
      <router-view v-else />
    </div>
    <Footer />
  </div>
  <LoginView v-else-if="isLogin" />
  <RegisterView v-else-if="isRegister" />
  <ResetPasswordView v-else-if="isResetPassword" />
  <SetPasswordView v-else-if="isSetPassword" />
  <VerificationView v-else-if="isVerification" />
  <BackgroundGraphs />
</template>

<script setup>
import BackgroundGraphs from "@/components/BackgroundGraphs.vue";
import Footer from "@/components/Footer.vue";
import Header from "@/components/Header.vue";
import Sidebar from "@/components/Sidebar.vue";
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
});
</script>

<style>
@import "@/assets/styles/css/bootstrap.min.css";
@import "@/assets/styles/css/main.css";

#app {
  font-family: "MesloLGS NF", sans-serif;
  /* font-family: "Arial", sans-serif; */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  height: 100%;
  width: 100%;
}
.main__content {
  background-color: rgba(30, 30, 35, 0.5);

  z-index: -50;
}

/* .card {
border: 1px solid var(--secondary);
} */

.btn {
  border-radius: 0.4rem !important;
}

.btn-check:focus + .btn,
.btn:focus {
  box-shadow: none;
}
</style>
