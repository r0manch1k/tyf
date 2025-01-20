<template>
  <div class="verification">
    <div
      class="verification__container flex row vh-100 align-items-center justify-content-center"
      style="min-height: 100vh"
    >
      <div
        class="verification__content col-12 row col-sm-8 col-md-6 col-lg-5 col-xl-4"
      >
        <Message
          :message="message"
          :show="showMessage"
          @update:show="showMessage = $event"
        />
        <div
          class="verification__box bg-secondary rounded p-4"
          style="border-radius: 1rem !important"
        >
          <div
            class="verification__header text-center align-items-center justify-content-between mb-2"
          >
            <h3 class="verification__title fs-5">Введите код подтверждения</h3>
          </div>
          <div
            class="verification__subheader text-center align-items-center justify-content-between mb-4"
          >
            <h3
              class="verification__subtitle fw-normal text-secondary-xx-light fs-6"
            >
              Код подтверждения был отправлен на вашу эл. почту
            </h3>
          </div>
          <form
            id="otp-form"
            method="post"
            role="form"
            v-on:submit.prevent="verifySubmit"
          >
            <div
              id="otp"
              class="verification__inputs inputs d-flex flex-row justify-content-center mt-2 mb-4"
            >
              <input
                v-for="(num, index) in otpNumbers"
                :key="index"
                class="verification__input m-2 text-center form-control rounded-3"
                style="border-radius: 0.8rem !important"
                :name="`otp_${index + 1}`"
                :id="`otp_${index + 1}`"
                maxlength="1"
                required
                v-model="otpNumbers[index]"
              />
            </div>
            <button
              type="submit"
              class="verification__submit btn btn-primary py-3 w-100 mb-3"
              :disabled="loading"
            >
              <label v-if="!loading" style="color: var(--dark) !important"
              >Подтвердить</label
              >
              <LoadingCircle v-else />
            </button>
          </form>
          <div class="verification__footer text-center">
            <span
              v-if="timerOn"
              class="verification__timer d-block text-center"
              ref="countdown"
            >
              Отправить новый код через
              {{
                countdownMinutes < 10
                  ? "0" + countdownMinutes
                  : countdownMinutes
              }}:{{
                countdownSeconds < 10
                  ? "0" + countdownSeconds
                  : countdownSeconds
              }}
            </span>
            <span v-else class="verification__resend d-block text-center">
              Не получили код?
              <a
                class="verification__resend-link text-color"
                ref="sendOtp"
                style="cursor: pointer !important"
                @click="startTimer(60, true)"
              >
                Отправить новый код
              </a>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import MessageModel from "@/models/MessageModel";
import AuthService from "@/services/AuthService";
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";

import LoadingCircle from "@/components/LoadingCircle.vue";
import Message from "@/components/Message.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();

const showErrorPage = ref(store.getters["error/getShowErrorPage"]);

const otpNumbers = ref(["", "", "", "", "", ""]);
const loading = ref(true);

const message = computed<MessageModel>(() => store.state.auth.message);
const showMessage = ref(false);

onMounted(async () => {
  loading.value = true;

  await AuthService.checkVerificationAccess(
    route.params.token as string,
    route.params.uid as string
  )
    .catch((error) => {
      store.commit("error/setShowErrorPage", error.status);
    })
    .finally(() => {
      loading.value = false;
    });

  if (!showErrorPage.value) {
    startTimer(60);
    OTPInput();
  }
});

const verifySubmit = async () => {
  loading.value = true;
  const otp = otpNumbers.value.join("");

  await AuthService.verify(
    otp,
    (route.params.token as string) ?? "",
    (route.params.uid as string) ?? ""
  )
    .then(() => {
      const message: MessageModel = {
        text: "Аккаунт успешно подтвержден.",
        type: "success",
      };
      store.commit("auth/setMessage", message);
      showMessage.value = true;
      router.push("/login");
    })
    .catch((error) => {
      if (error.status === 401) {
        const message: MessageModel = {
          text: "Ваша сессия подтверждения аккаунта истекла. Пройдите процесс регистрации заново.",
          type: "info",
        };
        store.commit("auth/setMessage", message);
        showMessage.value = true;
        router.push("/register");
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

const resendOTP = async () => {
  loading.value = true;

  await AuthService.resendOTP(
    (route.params.token as string) ?? "",
    (route.params.uid as string) ?? ""
  )
    .then(() => {
      const message: MessageModel = {
        text: "Новый код подтверждения был отправлен на вашу эл. почту.",
        type: "success",
      };
      store.commit("auth/setMessage", message);
    })
    .catch((error) => {
      if (error.status === 401) {
        store.commit("auth/setMessage", {
          text: "Ваша сессия подтверждения аккаунта истекла. Пройдите процесс регистрации заново.",
          type: "info",
        });
        router.push("/register");
      } else {
        store.commit("auth/setMessage", {
          text: "Что-то пошло не так, повторите попытку позже.",
          type: "error",
        });
      }
    })
    .finally(() => {
      loading.value = false;
    });
};

function OTPInput() {
  const inputs = document.querySelectorAll<HTMLInputElement>("#otp > *[id]");

  for (let i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener("keydown", function (event: KeyboardEvent) {
      if (
        (event.ctrlKey || event.metaKey) &&
        (event.key === "v" || event.key === "V")
      ) {
        return true;
      }

      if (event.key === "ArrowLeft") {
        if (i !== 0) inputs[i - 1].focus();
        event.preventDefault();
      } else if (event.key === "ArrowRight") {
        if (i !== inputs.length - 1) inputs[i + 1].focus();
        event.preventDefault();
      } else if (event.key === "Backspace") {
        event.preventDefault();
        otpNumbers.value[i] = "";
        inputs[i].value = "";
        if (i !== 0) inputs[i - 1].focus();
      } else if (event.key.length === 1) {
        if (event.key >= "0" && event.key <= "9") {
          otpNumbers.value[i] = event.key;
          inputs[i].value = event.key;
          if (i !== inputs.length - 1) inputs[i + 1].focus();
          event.preventDefault();
        } else if (event.key >= "A" && event.key <= "Z") {
          otpNumbers.value[i] = event.key.toUpperCase();
          inputs[i].value = event.key.toUpperCase();
          if (i !== inputs.length - 1) inputs[i + 1].focus();
          event.preventDefault();
        }
      }
    });

    inputs[i].addEventListener("paste", (event) => {
      event.preventDefault();
      if (event.clipboardData) {
        let data = event.clipboardData.getData("text/plain");
        let text_len = Math.min(data.length, inputs.length - i);

        for (let j = 0; j < text_len; j++) {
          otpNumbers.value[i + j] = data[j].toUpperCase();
          inputs[i + j].value = data[j].toUpperCase();
          if (i + j !== inputs.length - 1) inputs[i + j + 1].focus();
        }
      }
    });
  }
}

let timerOn = ref(true);
let countdownValue = ref(60);

const countdownMinutes = computed(() => Math.floor(countdownValue.value / 60));
const countdownSeconds = computed(() => countdownValue.value % 60);

async function startTimer(remaining: number, resend = false) {
  if (resend) {
    await resendOTP();
  }

  countdownValue.value = remaining;
  timerOn.value = true;

  const timer = setInterval(() => {
    if (countdownValue.value > 0) {
      countdownValue.value -= 1;
    } else {
      clearInterval(timer);
      timerOn.value = false;
    }
  }, 1000);
}
</script>

<style scoped>
.row > * {
  padding: 0;
}
</style>
