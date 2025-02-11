import router from "@/router";
import store from "@/stores";
import api from "@/stores/services/api";
import { AxiosResponse } from "axios";

class AuthService {
  getAccessTokenFromLocalStorage(): string {
    return localStorage.getItem("accessToken") ?? "n";
  }
  async handleOAuthRedirect(
    accessToken: string,
    provider: string
  ): Promise<void> {
    await api
      .post(`users/login/${provider}/`, {
        access_token: accessToken,
      })
      .then((response) => {
        if (response.status === 200) {
          localStorage.setItem(
            "accessToken",
            response.data.payload.token.access
          );
          localStorage.setItem(
            "refreshToken",
            response.data.payload.token.refresh
          );
        } else {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }

  async login(email: string, password: string): Promise<void> {
    await api
      .post("/users/login/", {
        email: email,
        password: password,
      })
      .then((response) => {
        if (response.status === 200) {
          localStorage.setItem(
            "accessToken",
            response.data.payload.token.access
          );
          localStorage.setItem(
            "refreshToken",
            response.data.payload.token.refresh
          );
        } else {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });

    await store.dispatch("profile/fetchProfile");
  }

  async logout(): Promise<void> {
    const refreshToken = localStorage.getItem("refreshToken") ?? "";

    if (refreshToken) {
      await api
        .post("/users/logout/", {
          token: { refresh: refreshToken },
        })
        .then((response) => {
          if (response.status == 200) {
            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");
          }
        })
        .catch((error) => {
          return Promise.reject(error);
        });
    }
  }

  async register(
    email: string,
    password1: string,
    password2: string
  ): Promise<void> {
    this.logout();

    await api
      .post("/users/register/", {
        email: email,
        password1: password1,
        password2: password2,
      })
      .then((response) => {
        if (response.status === 201) {
          router.push(
            `/verify/${response.data.payload.uid}/${response.data.payload.token}`
          );
        } else {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }

  async resetPassword(email: string): Promise<void> {
    await api
      .post("/users/reset-password/", {
        email: email,
      })
      .then((response) => {
        if (response.status === 201) {
          router.push(
            `/verify/${response.data.payload.uid}/${response.data.payload.token}`
          );
        } else {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }

  async checkPasswordResetAccess(token: string, uid: string): Promise<void> {
    await api
      .get("/users/set-password/", {
        params: {
          token: token,
          uid: uid,
        },
      })
      .then((response) => {
        if (response.status === 202) {
          return response;
        }
        return Promise.reject(response);
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }

  async setPassword(
    token: string,
    uid: string,
    password1: string,
    password2: string
  ): Promise<void> {
    await api
      .post(
        "/users/set-password/",
        {
          password1: password1,
          password2: password2,
        },
        {
          params: {
            token: token,
            uid: uid,
          },
        }
      )
      .then((response) => {
        if (response.status === 200) {
          return Promise.resolve(response);
        } else {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }

  async checkVerificationAccess(token: string, uid: string): Promise<void> {
    await api
      .get("/users/verification/", {
        params: {
          token: token,
          uid: uid,
        },
      })
      .then((response) => {
        if (response.status === 202) {
          return response;
        }
        return Promise.reject(response);
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }

  async verify(
    otp: string,
    token: string,
    uid: string
  ): Promise<AxiosResponse> {
    const response = await api.post(
      "/users/verification/",
      {
        otp: otp,
      },
      {
        params: {
          token: token,
          uid: uid,
        },
      }
    );

    if (response.status === 200 || response.status === 201) {
      return response;
    } else {
      throw response;
    }
  }

  async resendOTP(token: string, uid: string): Promise<void> {
    await api
      .patch("/users/verification/", "", {
        params: {
          token: token,
          uid: uid,
        },
      })
      .then((response) => {
        if (response.status === 200) {
          return response;
        }
        return Promise.reject(response);
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }
}

export default new AuthService();
