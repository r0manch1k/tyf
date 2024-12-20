<template>
  <div
    id="spinner"
    class="show bg-dark position-fixed translate-middle w-100 vh-100 top-50 start-50 d-flex flex-column align-items-center justify-content-center"
  >
    <div
      class="spinner-border text-primary"
      style="width: 3rem; height: 3rem; color: var(--primary) !important"
      role="status"
    ></div>
    <span class="sr-only ms-2 color-primary">Loading...</span>
  </div>
</template>
