<template>
  <Sidebar />
  <div class="content open">
    <Header />
    <!-- <WelcomeTitle /> -->
    <router-view />
    <Footer />
  </div>
</template>

<script lang="ts" setup></script>

<style scoped>
@import "@/assets/styles/css/bootstrap.min.css";
@import "@/assets/styles/css/style.css";
</style>
