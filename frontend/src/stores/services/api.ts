import store from "@/stores";
import axios from "axios";

const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  timeout: 50000,
  responseType: "json",
  responseEncoding: "utf8",
  headers: {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
    Accept: "application/json",
    "X-Api-Key": process.env.VUE_APP_API_KEY,
  },
  validateStatus: (status) => status < 500,
});

api.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem("accessToken") ?? "";
    // console.log(`Access token: ${accessToken}`);
    if (accessToken) {
      config.headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(async (response) => {
  if (response.status === 401 && response.data.code === "token_not_valid") {
    const originalRequest = response.config;
    try {
      await updateTokens();
      delete originalRequest.headers["Authorization"];
      return await api(originalRequest);
    } catch (updateError) {
      return Promise.reject(updateError);
    }
  } else if (response.status >= 404) {
    store.dispatch("error/setShowErrorPage", response.status);
  }
  return response;
});

const updateTokens = async () => {
  await api
    .post("/token/refresh/", {
      refresh: localStorage.getItem("refreshToken"),
    })
    .then((response) => {
      const newAccessToken = response.data.access;
      const newRefreshToken = response.data.refresh;
      localStorage.setItem("accessToken", newAccessToken);
      localStorage.setItem("refreshToken", newRefreshToken);
    })

    .catch((error) => {
      console.error("Ошибка при обновлении токена:", error);
    });
};

export default api;
