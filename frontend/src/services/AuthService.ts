import router from "@/router";
import store from "@/stores";
import api from "@/stores/services/api";

class AuthService {
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

    await store.dispatch("profile/fetchProfile");
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
        console.log("AuthService.ts", error);
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
          console.log(response);
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
          console.log(
            "AuthService.ts",
            response.data.payload.uid,
            response.data.payload.token
          );
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
    await store.dispatch("profile/fetchProfile");
  }

  async resetPassword(email: string): Promise<void> {
    await api
      .post("/users/reset-password/", {
        email: email,
      })
      .then((response) => {
        if (response.status === 201) {
          console.log(
            "AuthService.ts",
            response.data.payload.uid,
            response.data.payload.token
          );
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
        if (response.status === 200) {
          console.log("AuthService.ts", response.data.payload);
        } else {
          return Promise.reject(response);
        }
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
        "/users/set_password/",
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
          console.log("AuthService.ts", response.data.payload);
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
        if (response.status === 200) {
          console.log("AuthService.ts", response.data.payload);
        } else {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }

  async verify(otp: string, token: string, uid: string): Promise<void> {
    await api
      .post(
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
      )
      .then((response) => {
        if (response.status == 201) {
          const resetPasswordToken = response.data.payload.token ?? "";
          const uid = response.data.payload.uid ?? "";
          console.log(
            "AuthService.ts",
            resetPasswordToken,
            uid,
            resetPasswordToken && uid
          );

          if (resetPasswordToken && uid) {
            router.push(`/login/set_password/${uid}/${resetPasswordToken}`);
          } else {
            return Promise.reject(response);
          }
        } else if (response.status == 200) {
          return Promise.resolve(response);
        } else {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
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
          console.log("AuthService.ts", response.data.payload);
        } else {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }
}

export default new AuthService();
