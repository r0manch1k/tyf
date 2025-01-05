<template>
  <div
    class="footer container-fluid bg-secondary d-flex align-items-center justify-content-between p-3"
  >
    <div class="footer__authors text-sm-start fs-7 text-muted">
      <router-link :to="{ name: 'home' }">Tell Your Friends</router-link>,
      Правила.
    </div>
    <div class="footer__links d-flex align-items-center">
      <a
        href="https://github.com/r0manch1k/tyf"
        class="text-muted"
        target="_blank"
        rel="noopener noreferrer"
      >
        <i class="bi bi-github fs-4"></i>
      </a>
    </div>
  </div>
</template>

<style>
.footer {
  bottom: 0;
  width: 100%;
}
</style>
