import store from '@/stores'
import axios from 'axios'

const api = axios.create({
	baseURL: 'http://localhost:8000/api',
	timeout: 30000,
	responseType: 'json',
	responseEncoding: 'utf8',
	headers: {
		'X-Requested-With': 'XMLHttpRequest',
		'Content-Type': 'application/json',
		'X-Api-Key': 'cm4m0834.0a1KGd1nrdnbJl50yjkCnnqbHPuv5Xul',
	},
	validateStatus: status => status < 500,
})

api.interceptors.request.use(
	config => {
		const accessToken = localStorage.getItem('accessToken') ?? ''
		console.log(`Access token: ${accessToken}`)
		if (accessToken) {
			config.headers['Authorization'] = `Bearer ${accessToken}`
		}
		return config
	},
	error => {
		return Promise.reject(error)
	}
)

api.interceptors.response.use(async response => {
	if (response.status === 401 && response.data.code === 'token_not_valid') {
		const originalRequest = response.config
		try {
			await updateTokens()
			const accessToken = localStorage.getItem('accessToken')
			originalRequest.headers['Authorization'] = `Bearer ${accessToken}`
			return await api(originalRequest)
		} catch (updateError) {
			return Promise.reject(updateError)
		}
	} else if (response.status >= 400) {
		store.commit('main/setShowErrorPage', response.status)
	}
	return response
})

const updateTokens = async () => {
	await api
		.post('/token/refresh', {
			refresh: localStorage.getItem('refreshToken'),
		})
		.then(response => {
			const newAccessToken = response.data.access
			const newRefreshToken = response.data.refresh
			localStorage.setItem('accessToken', newAccessToken)
			localStorage.setItem('refreshToken', newRefreshToken)
		})

		.catch(error => {
			console.error('Ошибка при обновлении токена:', error)
		})
}

export default api
