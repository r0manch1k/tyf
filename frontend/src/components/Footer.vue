<template>
  <div class="container-fluid p-0 bottom-0 w-100">
    <div class="bg-dark rounded-top mt-4 p-0">
      <div
        class="container-fluid d-flex align-items-center justify-content-between p-4"
      >
        <div class="col-12 col-sm-6 text-center text-sm-start fs-9 text-muted">
          <router-link :to="{ name: 'home' }">Tell Your Friends</router-link>,
          All Right Reserved.
        </div>
        <div class="d-flex align-items-center gap-1">
          <a href="https://github.com/EmotionlessDev/tyf" class="text-muted">
            <i class="bi bi-github"></i>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
