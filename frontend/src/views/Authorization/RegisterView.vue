<template>
  <div :class="{ 'd-none': loading }">
    <div class="register-view container-fluid">
      <div
        class="register-view__wrapper flex row vh-100 align-items-center justify-content-center"
        style="min-height: 100vh"
      >
        <div
          class="register-view__content col-12 row col-sm-8 col-md-6 col-lg-5 col-xl-4"
        >
          <Message
            :message="message"
            :show="showMessage"
            @update:show="showMessage = $event"
          />
          <div
            class="register-view__form bg-dark-light rounded p-4"
            style="border-radius: 0.4rem !important"
          >
            <div
              class="register-view__header text-center align-items-center justify-content-between mb-4"
            >
              <h3
                class="register-view__title fs-5"
                style="color: var(--light) !important"
              >
                Зарегистрироваться в
                <router-link to="/">
                  <span
                    class="register-view__brand text-primary fs-5"
                    style="color: var(--primary) !important"
                    >tyf</span
                  >
                </router-link>
              </h3>
            </div>
            <OAuthButtons />
            <div class="register-view__separator col-md-12 mb-3">
              <div class="login-or">
                <hr class="hr-or" />
                <span class="span-or small" style="user-select: none">ИЛИ</span>
              </div>
            </div>
            <form
              method="post"
              role="form"
              v-on:submit.prevent="registerSubmit"
            >
              <div class="form-floating mb-2">
                <EmailField v-model="email" />
              </div>
              <div class="form-floating mb-2">
                <PasswordField v-model="password1" />
              </div>
              <div class="form-floating mb-3">
                <RepeatPasswordField v-model="password2" />
              </div>
              <button
                type="submit"
                class="register-view__submit btn btn-primary py-3 w-100 mb-4"
              >
                <label style="color: var(--dark) !important">Продолжить</label>
              </button>
            </form>
            <p class="register-view__login-link text-center mb-0">
              У вас уже есть аккаунт?
              <router-link to="/login"><span>Войти.</span></router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <LoadingCircle v-if="loading" />
</template>

<script lang="ts" setup>
import EmailField from "@/components/Authorization/Fields/EmailField.vue";
import PasswordField from "@/components/Authorization/Fields/PasswordField.vue";
import RepeatPasswordField from "@/components/Authorization/Fields/RepeatPasswordField.vue";
import OAuthButtons from "@/components/Authorization/OAuthButtons.vue";
import LoadingCircle from "@/components/LoadingCircle.vue";
import Message from "@/components/Message.vue";
import MessageModel from "@/models/MessageModel";
import AuthService from "@/services/AuthService";
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";

const store = useStore();

const email = ref("");
const password1 = ref("");
const password2 = ref("");
const loading = ref(false);

const message = computed<MessageModel>(() => store.state.auth.message);
const showMessage = ref(false);

onMounted(() => {
  const storeShowMessage = computed(() => {
    return store.getters["auth/getShowMessage"];
  });
  if (storeShowMessage.value) {
    showMessage.value = true;
    store.commit("auth/setShowMessage", false);
  }
});

const registerSubmit = async () => {
  loading.value = true;
  AuthService.register(email.value, password1.value, password2.value)
    .catch((error) => {
      const message: MessageModel = {
        text: error.data.message,
        type: "error",
      };
      store.commit("auth/setMessage", message);
      showMessage.value = true;
    })
    .finally(() => {
      loading.value = false;
    });
};
</script>

<style scoped>
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
