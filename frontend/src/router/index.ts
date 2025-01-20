import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/Authorization/LoginView.vue";
import RegisterView from "@/views/Authorization/RegisterView.vue";
import ResetPasswordView from "@/views/Authorization/ResetPasswordView.vue";
import SetPasswordView from "@/views/Authorization/SetPasswordView.vue";
import VerificationView from "@/views/Authorization/VerificationView.vue";
import NotFoundView from "@/views/NotFoundView.vue";
import ProfileView from "@/views/ProfileView.vue";
import PostDetailView from "@/views/PostDetailView.vue";
import PostCreateView from "@/views/PostCreateView.vue";
import ProfileEditView from "@/views/ProfileEditView.vue";
import LogoutView from "@/views/Authorization/LogoutView.vue";

import store from "@/stores";

const routes = [
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
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/login/reset_password",
    name: "reset-password",
    component: ResetPasswordView,
  },
  {
    path: "/login/set_password/:uid/:token",
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
