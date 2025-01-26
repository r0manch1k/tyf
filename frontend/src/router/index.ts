import GoogleAuthView from "@/views/Authorization/GoogleAuthView.vue";
import LoginView from "@/views/Authorization/LoginView.vue";
import LogoutView from "@/views/Authorization/LogoutView.vue";
import RegisterView from "@/views/Authorization/RegisterView.vue";
import ResetPasswordView from "@/views/Authorization/ResetPasswordView.vue";
import SetPasswordView from "@/views/Authorization/SetPasswordView.vue";
import VerificationView from "@/views/Authorization/VerificationView.vue";
import YandexAuthView from "@/views/Authorization/YandexAuthView.vue";
import HomeView from "@/views/HomeView.vue";
import NotFoundView from "@/views/NotFoundView.vue";
import PostCreateView from "@/views/PostCreateView.vue";
import ProfileEditView from "@/views/ProfileEditView.vue";
import PostDetailView from "@/views/PostDetailView.vue";
import ProfileView from "@/views/ProfileView.vue";
import ChatsView from "@/views/ChatsView.vue";
import NotificationsView from "@/views/NotificationsView.vue";

import store from "@/stores";
import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
  },
  {
    path: "/oauth/callback/google",
    name: "google-auth-callback",
    component: GoogleAuthView,
  },
  {
    path: "/oauth/callback/yandex",
    name: "yandex-auth-callback",
    component: YandexAuthView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/login/reset-password",
    name: "reset-password",
    component: ResetPasswordView,
  },
  {
    path: "/login/set-password/:uid/:token",
    name: "reset-password-confirm",
    component: SetPasswordView,
  },
  {
    path: "/verify/:uid/:token",
    name: "verification",
    component: VerificationView,
  },
  {
    path: "/edit",
    name: "profile-edit",
    component: ProfileEditView,
    beforeEnter: () => {
      if (store.getters["profile/getIsAuth"] === false) {
        return { name: "login" };
      }
    },
  },
  {
    path: "/chats",
    name: "chats",
    component: ChatsView,
    beforeEnter: () => {
      if (store.getters["profile/getIsAuth"] === false) {
        return { name: "login" };
      }
    },
  },
  {
    path: "/notifications",
    name: "notifications",
    component: NotificationsView,
    beforeEnter: () => {
      if (store.getters["profile/getIsAuth"] === false) {
        return { name: "login" };
      }
    },
  },
  {
    path: "/:username",
    name: "profile",
    component: ProfileView,
    props: true,
  },
  {
    path: "/posts/new",
    name: "post-create",
    component: PostCreateView,
    // beforeEnter: () => {
    //   console.log(store.getters["profile/getProfile"].id);
    //   if (
    //     store.getters["profile/getProfile"].id < 0 ||
    //     localStorage.getItem("accessToken") === ""
    //   ) {
    //     return { name: "login" };
    //   }
    // },
  },
  {
    path: "/posts/:identifier",
    name: "post-detail",
    component: PostDetailView,
    props: true,
  },
  {
    path: "/:catchAll(.*)",
    name: "NotFound",
    component: NotFoundView,
  },
  {
    path: "/logout",
    name: "logout",
    component: LogoutView,
    beforeEnter: () => {
      store.dispatch("profile/setDefault");
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.afterEach(() => {
  store.commit("error/setShowErrorPage", false);
});

export default router;
