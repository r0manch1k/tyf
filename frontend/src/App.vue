<template>
  <!-- TODO: Change v-if condition for isHome views -->
  <div v-if="isHome">
    <Header />
    <Sidebar />
    <router-view />
    <Footer />
  </div>
  <LoginView v-else-if="isLogin" />
  <RegisterView v-else-if="isRegister" />
  <ResetPasswordView v-else-if="isResetPassword" />
  <SetPasswordView v-else-if="isSetPassword" />
  <VerificationView v-else-if="isVerification" />
</template>

<script setup>
import Sidebar from "@/components/Sidebar.vue";
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import LoginView from "@/views/Authorization/LoginView.vue";
import RegisterView from "@/views/Authorization/RegisterView.vue";
import ResetPasswordView from "@/views/Authorization/ResetPasswordView.vue";
import SetPasswordView from "@/views/Authorization/SetPasswordView.vue";
import VerificationView from "@/views/Authorization/VerificationView.vue";
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const isLogin = computed(() => route.name === "login");
const isRegister = computed(() => route.name === "register");
const isResetPassword = computed(() => route.name === "reset_password");
const isSetPassword = computed(() => route.name === "reset_password_confirm");
const isVerification = computed(() => route.name === "verification");
const isHome = computed(
  () =>
    !isLogin.value &&
    !isRegister.value &&
    !isResetPassword.value &&
    !isSetPassword.value &&
    !isVerification.value
);
</script>

<style>
@import "@/assets/styles/css/bootstrap.min.css";
@import "@/assets/styles/css/main.css";

#app {
  font-family: "JetBrains Mono";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
  width: 100%;
}

a.router-link-exact-active {
  color: var(--light) !important;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
