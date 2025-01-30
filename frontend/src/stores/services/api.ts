import store from "@/stores";
import axios from "axios";

const api = axios.create({
  baseURL:
    process.env.NODE_ENV === "production"
      ? process.env.VUE_APP_HTTP_API_URL_PROD
      : process.env.VUE_APP_HTTP_API_URL_DEV,
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
    const refreshToken = localStorage.getItem("refreshToken");

    if (!refreshToken) {
      window.location.href = "/login";
      return Promise.reject(response);
    }

    try {
      const baseURL =
        process.env.NODE_ENV === "production"
          ? process.env.VUE_APP_HTTP_API_URL_PROD
          : process.env.VUE_APP_HTTP_API_URL_DEV;

      const refreshResponse = await axios.post(
        `${baseURL}/token/refresh/`,
        {
          refresh: refreshToken,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
            "X-Api-Key": process.env.VUE_APP_API_KEY,
          },
        }
      );

      const newAccessToken = refreshResponse.data.access;
      const newRefreshToken = refreshResponse.data.refresh;

      if (newAccessToken && newRefreshToken) {
        localStorage.setItem("accessToken", newAccessToken);
        localStorage.setItem("refreshToken", newRefreshToken);
        api.defaults.headers.common.Authorization = `Bearer ${newAccessToken}`;
      }

      return api(originalRequest);
    } catch (error) {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      window.location.href = "/login";
      return response;
    }
  } else if (response.status >= 404) {
    store.dispatch("error/setShowErrorPage", response.status);
  }
  return response;
});

export default api;
