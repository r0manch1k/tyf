<template>
  <div>
    <a
      href="{% url 'social:begin' 'google-oauth2' %}"
      class="btn btn-dark border rounded-pill px-4 py-2 mb-2 w-100"
    >
      <img
        src="https://img.icons8.com/color/48/000000/google-logo.png"
        class="rounded float-start"
        width="24"
        height="24"
      />
      <span class="text-center" style="margin: 0% !important"
        >Continue with Google</span
      >
    </a>
    <a
      href="{% url 'social:begin' 'yandex-oauth2' %}"
      class="btn btn-dark border rounded-pill px-4 py-2 mb-2 w-100"
    >
      <img
        src="https://upload.wikimedia.org/wikipedia/commons/5/58/Yandex_icon.svg"
        class="rounded float-start"
        width="24"
        height="24"
      />
      <span class="text-center" style="margin: 0% !important"
        >Continue with Yandex</span
      >
    </a>
  </div>
</template>
