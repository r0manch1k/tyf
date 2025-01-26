<template>
  <canvas id="background"></canvas>
</template>

<script setup>
import { onMounted } from "vue";

onMounted(() => {
  const script = document.createElement("script");
  script.setAttribute("src", require("@/assets/styles/js/background.js"));
  script.setAttribute("type", "text/javascript");
  document.head.appendChild(script);
});
</script>

<style>
canvas {
  position: fixed;
  top: 0;
  left: 0;
  background-color: var(--dark);
  z-index: -100;
}
</style>
