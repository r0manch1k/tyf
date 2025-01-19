<template>
  <div>
    <a
      @click="loginWithGoogle"
      class="btn btn-dark border rounded-pill px-4 py-2 mb-2 w-100"
    >
      <img
        src="https://img.icons8.com/color/48/000000/google-logo.png"
        class="rounded float-start"
        width="24"
        height="24"
      />
      <span
        class="text-center"
        style="margin: 0% !important; color: var(--light)"
        >Продолжить с Google</span
      >
    </a>
    <a
      @click="loginWithYandex"
      class="btn btn-dark border rounded-pill px-4 py-2 mb-2 w-100"
    >
      <img
        src="https://upload.wikimedia.org/wikipedia/commons/5/58/Yandex_icon.svg"
        class="rounded float-start"
        width="24"
        height="24"
      />
      <span
        class="text-center"
        style="margin: 0% !important; color: var(--light)"
        >Продолжить с Яндекс</span
      >
    </a>
  </div>
</template>

<script lang="ts">
import api from "@/stores/services/api";
import { defineComponent } from "vue";

export default defineComponent({
  methods: {
    async loginWithGoogle() {
      const googleAuthUrl = "https://accounts.google.com/o/oauth2/auth";
      const clientId = process.env.VUE_APP_GOOGLE_OAUTH2_CLIENT_ID;
      const redirectUri = window.location.href;
      const responseType = "token";
      const scope = "email profile";
      const prompt = "select_account+consent";

      const url = `${googleAuthUrl}?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}&prompt=${prompt}`;
      window.location.href = url;
    },
    async loginWithYandex() {
      const yandexAuthUrl = "https://oauth.yandex.ru/authorize";
      const clientId = process.env.VUE_APP_YANDEX_OAUTH2_CLIENT_ID;
      const redirectUri = window.location.href;
      const responseType = "token";
      const scope = "login:info login:email";
      const forceConfirm = "true";

      const url = `${yandexAuthUrl}?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}&force_confirm=${forceConfirm}`;
      window.location.href = url;
    },
    async handleRedirect() {
      const hash = window.location.hash;
      console.log(hash);

      // TODO: make endpoints for oauth callbacks
      if (hash) {
        const token = hash.split("&")[0].split("=")[1];
        await api
          .post("users/login/google/", {
            access_token: token,
          })
          .then((response) => {
            console.log(response.data.payload.token.access);
          })
          .catch(() => {
            this.$emit("loading", false);
          });
        // if (
        // 	hash.split('&')[0].split('=')[0] == 'access_token' &&
        // 	hash.split('&')[-1].split('=')[0] == 'cid'
        // ) {
        // 	const token = hash.split('&')[0].split('=')[1]
        // 	await api
        // 		.post('users/login/yandex/', {
        // 			access_token: token,
        // 		})
        // 		.then(response => {
        // 			console.log(response.data.payload.token.access)
        // 		})
        // 		.catch(() => {
        // 			this.$emit('loading', false)
        // 		})
        // }
        // if (
        // 	hash.split('&')[0].split('=')[0] == 'access_token' &&
        // 	hash.split('&')[-1].split('=')[0] == 'prompt'
        // ) {
        // 	const token = hash.split('&')[0].split('=')[1]
        // 	await api
        // 		.post('users/login/google/', {
        // 			access_token: token,
        // 		})
        // 		.then(response => {
        // 			console.log(response.data.payload.token.access)
        // 		})
        // 		.catch(() => {
        // 			this.$emit('loading', false)
        // 		})
        // }
      }
    },
  },
  mounted() {
    this.handleRedirect();
  },
});
</script>
