<template>
  <div
    class="footer container-fluid bg-dark-light d-flex align-items-center justify-content-between p-4"
  >
    <div class="footer__authors text-sm-start fs-6 text-muted">
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

<style scoped>
.footer {
  bottom: 0;
  width: 100%;
  /* border-top: 1px solid var(--secondary); */
}

a {
  color: var(--light);
}
</style>
