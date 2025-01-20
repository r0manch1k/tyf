<template>
  <div>
    <a
      @click="submitGoogleAuth"
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
      @click="submitYandexAuth"
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

<script lang="ts" setup>
const submitGoogleAuth = () => {
  const googleAuthUrl = "https://accounts.google.com/o/oauth2/auth";
  const clientId = process.env.VUE_APP_GOOGLE_OAUTH2_CLIENT_ID;
  const responseType = "token";
  const scope = "email+profile";
  const prompt = "select_account+consent";
  const redirectUri = `${window.location.origin}/oauth/callback/google`

  const url = `${googleAuthUrl}?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}&prompt=${prompt}`;
  console.log(url);
  window.location.href = url;
};

const submitYandexAuth = () => {
  const yandexAuthUrl = "https://oauth.yandex.ru/authorize";
  const clientId = process.env.VUE_APP_YANDEX_OAUTH2_CLIENT_ID;
  const responseType = "token";
  const scope = "login:info login:email";
  const forceConfirm = "true";
  const redirectUri = `${window.location.origin}/oauth/callback/yandex`

  const url = `${yandexAuthUrl}?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}&force_confirm=${forceConfirm}`;
  window.location.href = url;
};
</script>
