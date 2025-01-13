<template>
  <NotFoundView v-if="showErrorPage" />
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
						<h3 class="fs-5">Введите новый пароль</h3>
					</div>
					<form
						method="post"
						role="form"
						v-on:submit.prevent="setPasswordSubmit"
					>
						<div class="form-floating mb-2">
							<PasswordField v-model="password" />
						</div>
						<div class="form-floating mb-3">
							<RepeatPasswordField v-model="repeatPassword" />
						</div>
						<button
							type="submit"
							class="btn btn-primary py-3 w-100 mb-2"
							style="border-radius: 1rem !important"
						>
							<label style="color: var(--dark) !important">Продолжить</label>
						</button>
					</form>
				</div>
			</div>
		</div>
	</div>
	<LoadingCircle v-if="loading" />
</template>

<script lang="ts" setup>
import store from '@/stores'
import api from '@/stores/services/api'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import PasswordField from '@/components/Authorization/Fields/PasswordField.vue'
import RepeatPasswordField from '@/components/Authorization/Fields/RepeatPasswordField.vue'
import LoadingCircle from '@/components/LoadingCircle.vue'
import Messages from '@/components/Authorization/Messages.vue'
import NotFoundView from '@/views/NotFoundView.vue'

interface MessagesComponent {
	addMessage: (message: { type: string; text: string }) => void
}

const route = useRoute()
const router = useRouter()

const password = ref('')
const repeatPassword = ref('')
const loading = ref(true)
const showErrorPage = ref(false)
const messagesComponent = ref<MessagesComponent | null>(null)

onMounted(async () => {
	await api
		.get('users/set_password/', {
			params: {
				token: route.params.token ?? '',
				uid: route.params.uid ?? '',
			},
		})
		.then(response => {
			console.log(response)
			if (response.status >= 400) {
				showErrorPage.value = true
			}
		})
		.catch(() => {
			showErrorPage.value = true
		})
	loading.value = false
})

const setPasswordSubmit = async () => {
	loading.value = true

	await api
		.post(
			'users/set_password/',
			{
				password1: password.value,
				password2: repeatPassword.value,
			},
			{
				params: {
					token: route.params.token ?? '',
					uid: route.params.uid ?? '',
				},
			}
		)
		.then(response => {
			loading.value = false
			if (response.status == 200) {
				store.commit('main/setAuthMessage', {
					text: response.data.message,
					type: 'success',
				})
				router.push('/login')
			} else if (response.status == 401) {
				store.commit('main/setAuthMessage', {
					text: 'Ваша сессия смены пароля истекла. Пройдите процесс смены пароля заново.',
					type: 'info',
				})
				router.push('/login')
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
		.catch(() => {
			loading.value = false
			if (messagesComponent.value) {
				messagesComponent.value.addMessage({
					type: 'error',
					text: 'Что-то пошло не так, повторите попытку позже.',
				})
			}
		})
}
</script>

<style scoped></style>
