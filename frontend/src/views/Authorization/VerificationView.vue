<template>
	<NotFoundView v-if="showErrorPage" />
	<div :class="{ 'd-none': loading }">
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
						class="text-center align-items-center justify-content-between mb-2"
					>
						<h3 class="fs-5">Введите код подтверждения</h3>
					</div>
					<div
						class="text-center align-items-center justify-content-between mb-4"
					>
						<h3 class="fs-6" style="color: #aeadad !important">
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
							class="inputs d-flex flex-row justify-content-center mt-2 mb-4"
						>
							<input
								v-for="(num, index) in otpNumbers"
								:key="index"
								class="m-2 text-center form-control rounded-3"
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
							class="btn btn-primary py-3 w-100 mb-3"
							style="border-radius: 1rem !important"
						>
							<label style="color: var(--dark) !important">Подтвердить</label>
						</button>
					</form>
					<div class="text-center">
						<span v-if="timerOn" class="d-block text-center" ref="countdown">
							Отправить новый код через
							{{
								countdownMinutes < 10
									? '0' + countdownMinutes
									: countdownMinutes
							}}:{{
								countdownSeconds < 10
									? '0' + countdownSeconds
									: countdownSeconds
							}}
						</span>
						<span v-else class="d-block text-center">
							Не получили код?
							<a
								class="text-color"
								ref="sendOtp"
								style="cursor: pointer !important"
								@click="startTimer(60, true)"
								>Отправить новый код</a
							>
						</span>
					</div>
				</div>
			</div>
		</div>
	</div>
	<LoadingCircle v-if="loading" />
</template>

<script lang="ts" setup>
import store from '@/stores'
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Messages from '@/components/Authorization/Messages.vue'
import LoadingCircle from '@/components/LoadingCircle.vue'
import api from '@/stores/services/api'
import NotFoundView from '@/views/NotFoundView.vue'

interface MessagesComponent {
	addMessage: (message: { type: string; text: string }) => void
}

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const showErrorPage = ref(false)
const otpNumbers = ref(['', '', '', '', '', ''])
const messagesComponent = ref<MessagesComponent | null>(null)

onMounted(async () => {
	await api
		.get('users/verification/', {
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

	if (!showErrorPage.value) {
		startTimer(60)
		OTPInput()
	}
})

const verifySubmit = async () => {
	loading.value = true
	const otp = otpNumbers.value.join('')

	await api
		.post(
			'users/verification/',
			{
				otp: otp,
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
			console.log(response.status, response.status == 201)
			if (response.status == 200) {
				store.commit('main/setAuthMessage', {
					text: response.data.message,
					type: 'success',
				})
				router.push('/login')
			} else if (response.status == 201) {
				const resetPasswordToken = response.data.payload.token ?? ''
				const uid = response.data.payload.uid ?? ''
				console.log(resetPasswordToken, uid, resetPasswordToken && uid)
				if (resetPasswordToken && uid) {
					router.push(`/login/set_password/${uid}/${resetPasswordToken}`)
				} else {
					store.commit('main/setAuthMessage', {
						text: 'Что-то пошло не так. Пройдите процесс смены пароля заново.',
						type: 'info',
					})
					router.push('login/')
				}
			} else if (response.status == 401) {
				store.commit('main/setAuthMessage', {
					text: 'Ваша сессия подтверждения аккаунта истекла. Пройдите процесс регистрации заново.',
					type: 'info',
				})
				router.push('/register')
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

const resendOTP = async () => {
	loading.value = true

	await api
		.patch('users/verification/', '', {
			params: {
				token: route.params.token ?? '',
				uid: route.params.uid ?? '',
			},
		})
		.then(response => {
			loading.value = false
			if (response.status == 200) {
				const successMessage = response?.data?.message ?? ''
				if (messagesComponent.value) {
					messagesComponent.value.addMessage({
						type: 'success',
						text: successMessage,
					})
				}
			} else if (response.status == 401) {
				store.commit('main/setAuthMessage', {
					text: 'Ваша сессия подтверждения аккаунта истекла. Пройдите процесс регистрации заново.',
					type: 'info',
				})
				router.push('/register')
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

function OTPInput() {
	const inputs = document.querySelectorAll<HTMLInputElement>('#otp > *[id]')

	for (let i = 0; i < inputs.length; i++) {
		inputs[i].addEventListener('keydown', function (event: KeyboardEvent) {
			if (
				(event.ctrlKey || event.metaKey) &&
				(event.key === 'v' || event.key === 'V')
			) {
				return true
			}

			if (event.key === 'ArrowLeft') {
				if (i !== 0) inputs[i - 1].focus()
				event.preventDefault()
			} else if (event.key === 'ArrowRight') {
				if (i !== inputs.length - 1) inputs[i + 1].focus()
				event.preventDefault()
			} else if (event.key === 'Backspace') {
				event.preventDefault()
				otpNumbers.value[i] = ''
				inputs[i].value = ''
				if (i !== 0) inputs[i - 1].focus()
			} else if (event.key.length === 1) {
				if (event.key >= '0' && event.key <= '9') {
					otpNumbers.value[i] = event.key
					inputs[i].value = event.key
					if (i !== inputs.length - 1) inputs[i + 1].focus()
					event.preventDefault()
				} else if (event.key >= 'A' && event.key <= 'Z') {
					otpNumbers.value[i] = event.key.toUpperCase()
					inputs[i].value = event.key.toUpperCase()
					if (i !== inputs.length - 1) inputs[i + 1].focus()
					event.preventDefault()
				}
			}
		})

		inputs[i].addEventListener('paste', event => {
			event.preventDefault()
			if (event.clipboardData) {
				let data = event.clipboardData.getData('text/plain')
				let text_len = Math.min(data.length, inputs.length - i)

				for (let j = 0; j < text_len; j++) {
					otpNumbers.value[i + j] = data[j].toUpperCase()
					inputs[i + j].value = data[j].toUpperCase()
					if (i + j !== inputs.length - 1) inputs[i + j].focus()
				}

				console.log(data, text_len)
			}
		})
	}
}

let timerOn = ref(true)
let countdownValue = ref(60)

const countdownMinutes = computed(() => Math.floor(countdownValue.value / 60))
const countdownSeconds = computed(() => countdownValue.value % 60)

async function startTimer(remaining: number, resend = false) {
	if (resend) {
		await resendOTP()
	}

	countdownValue.value = remaining
	timerOn.value = true

	const timer = setInterval(() => {
		if (countdownValue.value > 0) {
			countdownValue.value -= 1
		} else {
			clearInterval(timer)
			timerOn.value = false
		}
	}, 1000)
}
</script>
