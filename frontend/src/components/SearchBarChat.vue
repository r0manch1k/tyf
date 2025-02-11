<template>
  <div class="search-bar-chat py-2 fs-6">
    <input
      type="text"
      class="search-bar-chat__input form-control fs-6 border-0"
      placeholder="Поиск"
    />
  </div>
</template>

<script lang="ts" setup></script>

<style scoped>
.search-bar-chat__input {
  background-color: var(--dark-light) !important;
  border-radius: 0.4em !important;
  box-shadow: none !important;
}

.search-bar-chat__input:focus {
  color: var(--light) !important;
  background-color: var(--secondary) !important;
  outline: none !important;
}

input[type="search"]::-webkit-search-cancel-button {
  -webkit-appearance: none;
  appearance: none;
}
</style>
