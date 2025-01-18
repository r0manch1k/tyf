<template>
  <div>
    <a
      href="{% url 'social:begin' 'google-oauth2' %}"
      class="btn btn-dark border px-4 py-2 mb-2 w-100"
      style="border-radius: 0.4rem"
    >
      <img
        src="https://img.icons8.com/color/48/000000/google-logo.png"
        class="float-start"
        style="border-radius: 0.4rem"
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
      href="{% url 'social:begin' 'yandex-oauth2' %}"
      class="btn btn-dark border px-4 py-2 mb-2 w-100"
      style="border-radius: 0.4rem"
    >
      <img
        src="https://upload.wikimedia.org/wikipedia/commons/5/58/Yandex_icon.svg"
        class="float-start"
        style="border-radius: 0.4rem"
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
