<template>
  <div class="container-fluid position-relative d-flex p-0">
    <!-- <LoadingCircle /> -->
    <Sidebar />
    <div class="content open">
      <Header />
      <WelcomeTitle />
      <Footer />
    </div>
  </div>
</template>

<script lang="ts" setup>
import LoadingCircle from "@/components/LoadingCircle.vue";
import Sidebar from "@/components/Sidebar.vue";
import Header from "@/components/Header.vue";
import WelcomeTitle from "@/components/WelcomeTitle.vue";
import Footer from "@/components/Footer.vue";
</script>