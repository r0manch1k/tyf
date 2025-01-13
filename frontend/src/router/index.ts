import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/Authorization/LoginView.vue";
import RegisterView from "@/views/Authorization/RegisterView.vue";
import ResetPasswordView from "@/views/Authorization/ResetPasswordView.vue";
import SetPasswordView from "@/views/Authorization/SetPasswordView.vue";
import VerificationView from "@/views/Authorization/VerificationView.vue";
import ProfileView from "@/views/ProfileView.vue";
import PostDetailView from "@/views/PostDetailView.vue";
import PostCreateView from "@/views/PostCreateView.vue";
import ProfileEdit from "@/views/ProfileEdit.vue";
import store from "@/stores";

// TODO: Change _ to - in router names

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
    path: "/edit",
    name: "profile-edit",
    component: ProfileEdit,
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
  },
  {
    path: "/posts/:identifier",
    name: "post-detail",
    component: PostDetailView,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// router.beforeEach((to, from, next) => {
//   store.commit("main/setShowErrorPage", false);
//   next();
// });

// TODO: In all tutorials they use beforeEach, but here's the big problem i can explain you
// So I use afterEach
router.afterEach(() => {
  store.commit("main/setShowErrorPage", false);
});

export default router;
