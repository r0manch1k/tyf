import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";

const app = createApp(App);
const axiosInstance = axios.create({
  baseURL: "https://localhost:8000/api",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
});

app.provide("$axios", axiosInstance);
// app.config.globalProperties.$axios = axiosInstance;

app.use(store).use(router).mount("#app");
