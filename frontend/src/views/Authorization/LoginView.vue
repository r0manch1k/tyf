<template>
  <div class="container-fluid">
    <div
      class="flex row vh-100 align-items-center justify-content-center"
      style="min-height: 100vh"
    >
      <div class="col-12 row col-sm-8 col-md-6 col-lg-5 col-xl-4">
        <!-- TODO: ADD MESSAGES -->
        <div
          class="bg-secondary rounded p-4"
          style="border-radius: 1rem !important"
        >
          <div
            class="text-center align-items-center justify-content-between mb-4"
          >
            <h3 class="fs-5">
              Sign In to
              <router-link to="/">
                <a class="fs-5" style="font-family: 'Roboto' !important"
                  >Tell Your Friends</a
                >
              </router-link>
            </h3>
          </div>
          <OAuthButtons />
          <div class="col-md-12 mb-3">
            <div class="login-or">
              <hr class="hr-or" />
              <span class="span-or small">OR</span>
            </div>
          </div>
          <form method="post" role="form">
            <div class="form-floating mb-2">
              <EmailField />
            </div>
            <div class="form-floating mb-3">
              <PasswordField />
            </div>
            <router-link to="/login/reset_password">
              <div
                class="d-flex align-items-center justify-content-between mb-3"
              >
                <a>Forgot password?</a>
              </div>
            </router-link>
            <button
              type="submit"
              class="btn btn-primary py-3 w-100 mb-4"
              style="border-radius: 1rem !important"
            >
              <label style="color: var(--dark) !important">Sign In</label>
            </button>
          </form>
          <p class="text-center mb-0">
            Don't have an Account?
            <router-link to="/register"><a>Sign Up</a></router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import OAuthButtons from "@/components/Authorization/OAuthButtons.vue";
import EmailField from "@/components/Authorization/Fields/EmailField.vue";
import PasswordField from "@/components/Authorization/Fields/PasswordField.vue";
</script>

<style scoped>
@import "@/assets/styles/css/bootstrap.min.css";
@import "@/assets/styles/css/style.css";
</style>
