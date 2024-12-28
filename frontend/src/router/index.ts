import { createRouter, createWebHistory } from "vue-router";
import IndexView from "../views/IndexView.vue";
import NotFoundView from "../views/NotFoundView.vue";
import LoginView from "../views/Authorization/LoginView.vue";
import RegisterView from "../views/Authorization/RegisterView.vue";
import ResetPasswordView from "../views/Authorization/ResetPasswordView.vue";
import SetPasswordView from "@/views/Authorization/SetPasswordView.vue";
import VerificationView from "@/views/Authorization/VerificationView.vue";
import ProfileView from "@/views/ProfileView.vue";

const routes = [
  {
    path: "/",
    name: "index",
    component: IndexView,
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
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/login/reset_password",
    name: "reset_password",
    component: ResetPasswordView,
  },
  {
    // path: "/login/set_password/:uid/:token",
    path: "/login/set_password",
    name: "reset_password_confirm",
    component: SetPasswordView,
  },
  {
    // path: "/verify/:uid/:token",
    path: "/verify",
    name: "verification",
    component: VerificationView,
  },
  {
    path: "/:username",
    name: "profile",
    component: ProfileView,
    props: true,
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: NotFoundView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
