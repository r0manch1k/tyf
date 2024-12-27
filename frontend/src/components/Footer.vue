<template>
  <div
    class="footer container-fluid bg-secondary d-flex align-items-center justify-content-between p-4"
  >
    <div class="footer__authors text-sm-start fs-7 text-muted">
      <router-link :to="{ name: 'home' }">Tell Your Friends</router-link>, All
      Right Reserved.
    </div>
    <div class="footer__links d-flex align-items-center">
      <a href="https://github.com/EmotionlessDev/tyf" class="text-muted">
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
