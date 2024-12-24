<template>
  <!-- <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </nav> -->
  <!-- <IndexView /> -->
  <router-view />
</template>

<script setup>
import IndexView from "@/views/IndexView.vue";
</script>

<style>
@import "@/assets/styles/css/bootstrap.min.css";
@import "@/assets/styles/css/edit_profile.css";
@import "@/assets/styles/css/post_add.css";
@import "@/assets/styles/css/post_detail.css";
@import "@/assets/styles/css/post_edit.css";
@import "@/assets/styles/css/post.css";
@import "@/assets/styles/css/profile.css";
@import "@/assets/styles/css/style.css";

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
