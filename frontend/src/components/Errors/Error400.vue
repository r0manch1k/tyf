<template>
  <div
    class="flex row vh-100 align-items-center justify-content-center"
    style="min-height: 100vh"
  >
    <div
      class="row vh-100 rounded align-items-center justify-content-center mx-0"
    >
      <div class="col-md-6 text-center p-4">
        <i class="bi bi-exclamation-triangle display-1 text-primary"></i>
        <h1 class="display-1 fw-bold">400</h1>
        <h1 class="mb-4">Bad Request</h1>
        <p class="mb-4">
          The server encountered an error while processing your request. Please
          try again later.
        </p>
        <router-link to="/">
          <a class="btn btn-primary rounded-pill py-3 px-5"
            ><label style="color: var(--dark) !important"
              >Go to Tell Your Friends</label
            ></a
          >
        </router-link>
      </div>
    </div>
  </div>
</template>
