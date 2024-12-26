<template>
  <div
    class="flex row vh-100 align-items-center justify-content-center"
    style="min-height: 100vh"
  >
    <div class="col-12 row col-sm-8 col-md-6 col-lg-5 col-xl-4">
      <div
        id="msg"
        style="
          margin: 0 !important;
          padding-right: 0 !important;
          padding-left: 0 !important;
        "
      ></div>
      <div
        class="bg-secondary rounded p-4"
        style="border-radius: 1rem !important"
      >
        <div
          class="text-center align-items-center justify-content-between mb-2"
        >
          <h3 class="fs-5">Enter verification code</h3>
        </div>
        <div
          class="text-center align-items-center justify-content-between mb-4"
        >
          <h3 class="fs-6" style="color: #aeadad !important">
            A code has been sent to {{ user_email }}
          </h3>
        </div>
        <form id="otp-form" method="post" role="form">
          <div
            id="otp"
            class="inputs d-flex flex-row justify-content-center mt-2 mb-4"
          >
            <input
              class="m-2 text-center form-control rounded-3"
              style="border-radius: 0.8rem !important"
              name="1"
              id="1"
              maxlength="1"
              required
              aria-invalid="true"
            />
            <input
              class="m-2 text-center form-control rounded-3"
              style="border-radius: 0.8rem !important"
              name="2"
              id="2"
              maxlength="1"
              required
              aria-invalid="true"
            />
            <input
              class="m-2 text-center form-control rounded-3"
              style="border-radius: 0.8rem !important"
              name="3"
              id="3"
              maxlength="1"
              required
              aria-invalid="true"
            />
            <input
              class="m-2 text-center form-control rounded-3"
              style="border-radius: 0.8rem !important"
              name="4"
              id="4"
              maxlength="1"
              required
              aria-invalid="true"
            />
            <input
              class="m-2 text-center form-control rounded-3"
              style="border-radius: 0.8rem !important"
              name="5"
              id="5"
              maxlength="1"
              required
              aria-invalid="true"
            />
            <input
              class="m-2 text-center form-control rounded-3"
              style="border-radius: 0.8rem !important"
              name="6"
              id="6"
              maxlength="1"
              required
              aria-invalid="true"
            />
          </div>
          <button
            type="submit"
            class="btn btn-primary py-3 w-100 mb-3"
            style="border-radius: 1rem !important"
          >
            <label style="color: var(--dark) !important">Confirm</label>
          </button>
        </form>
        <form id="otp-resend-form" method="post" role="form">
          <input type="hidden" id="send-status" name="send-status" value="1" />
          <div class="text-center">
            <span
              class="d-block text-center"
              id="countdown"
              style="margin: 0 !important"
            >
              Send new code
            </span>
            <span class="d-block text-center" id="resend"></span>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import "@/assets/styles/js/otp.js";
import "@/assets/styles/js/timer.js";
</script>
