<template>
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
					<div
						class="text-center align-items-center justify-content-between mb-4"
					>
						<h3 class="fs-5" style="color: var(--light) !important">
							Войти в аккаунт
							<router-link to="/">
								<span
									class="text-primary fs-5"
									style="
										color: var(--primary) !important;
										font-family: 'Roboto' !important;
									"
									>Tell Your Friends</span
								>
							</router-link>
						</h3>
					</div>
					<OAuthButtons />
					<div class="col-md-12 mb-3">
						<div class="login-or">
							<hr class="hr-or" />
							<span class="span-or small" style="user-select: none">ИЛИ</span>
						</div>
					</div>
					<form method="post" role="form" @submit.prevent="loginSubmit">
						<div class="form-floating mb-2">
							<EmailField v-model="email" />
						</div>
						<div class="form-floating mb-3">
							<PasswordField v-model="password" />
						</div>
						<router-link to="/login/reset_password">
							<div
								class="d-flex align-items-center justify-content-between mb-3"
							>
								<a>Забыли пароль?</a>
							</div>
						</router-link>
						<button
							type="submit"
							class="btn btn-primary py-3 w-100 mb-4"
							style="border-radius: 1rem !important"
						>
							<label style="color: var(--dark) !important">Войти</label>
						</button>
					</form>
					<p class="text-center mb-0">
						У вас нет аккаунта?
						<router-link to="/register"><a>Зарегистрироваться.</a></router-link>
					</p>
				</div>
			</div>
		</div>
	</div>
	<LoadingCircle v-if="loading" />
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'
import store from '@/stores'
import api from '@/stores/services/api'
import { useRouter } from 'vue-router'

import EmailField from "@/components/Authorization/Fields/EmailField.vue";
import PasswordField from "@/components/Authorization/Fields/PasswordField.vue";
import OAuthButtons from "@/components/Authorization/OAuthButtons.vue";
import Messages from '@/components/Authorization/Messages.vue'
import LoadingCircle from '@/components/LoadingCircle.vue'

interface MessagesComponent {
	addMessage: (message: { type: string; text: string }) => void
}
interface AuthMessageInterface {
	text: string
	type: string
}

const router = useRouter()

const email = ref('')
const password = ref('')
const loading = ref(false)
const messagesComponent = ref<MessagesComponent | null>(null)

onMounted(() => {
	const authMessage = computed(
		// @ts-expect-error: Unreachable code error
		() => store.state.main.authMessage as AuthMessageInterface
	)

	if (messagesComponent.value && authMessage.value) {
		messagesComponent.value.addMessage({
			type: authMessage.value.type,
			text: authMessage.value.text,
		})
	}
	store.commit('main/setAuthMessage', {
		text: '',
		type: '',
	})
})

const loginSubmit = async () => {
  loading.value = true

  await api
   .post('users/login/', {
      email: email.value,
      password: password.value,
    })
    .then((response) => {
      loading.value = false
      if (response.status === 200) {
        localStorage.setItem('accessToken', response.data.payload.token.access)
        localStorage.setItem('refreshToken', response.data.payload.token.refresh)
				router.push("/")
			} else {
				const errorMessage =
					response?.data?.message ||
					'Что-то пошло не так, повторите попытку позже.'
				if (messagesComponent.value) {
					messagesComponent.value.addMessage({
						type: 'error',
						text: errorMessage,
					})
				}
			}
    })
    .catch((error) => {
      loading.value = false
      const errorMessage =
        error?.response?.data?.message ||
        'Что-то пошло не так, повторите попытку позже.'
      if (messagesComponent.value) {
        messagesComponent.value.addMessage({
          type: 'error',
          text: errorMessage,
        })
      }
    })
}
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
	background-color: var(--secondary);
	width: 50px;
	text-align: center;
}

.hr-or {
	height: 1px;
	margin-top: 0px !important;
	margin-bottom: 0px !important;
}
</style>
