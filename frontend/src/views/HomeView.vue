<template>
  <Sidebar />
  <div class="content open">
    <Header />
    <WelcomeTitle />
    <Footer />
  </div>
</template>

<script lang="ts" setup>
import Sidebar from "@/components/Sidebar.vue";
import Header from "@/components/Header.vue";
import WelcomeTitle from "@/components/WelcomeTitle.vue";
import Footer from "@/components/Footer.vue";
</script>

<style scoped>
@import "@/assets/styles/css/bootstrap.min.css";
@import "@/assets/styles/css/style.css";
</style>
