import axios from "axios";
import store from "@/stores";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  timeout: 30000,
  responseType: "json",
  responseEncoding: "utf8",
  headers: {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  },
  validateStatus: (status) => status < 500,
});

api.interceptors.response.use((response) => {
  if (response.status >= 400) {
    store.commit("main/setShowErrorPage", response.status);
  }
  return response;
});

export default api;
