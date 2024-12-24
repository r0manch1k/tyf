<template>
  <div class="container-fluid">
    <div
      class="flex row vh-100 align-items-center justify-content-center"
      style="min-height: 100vh"
    >
      <div class="col-12 row col-sm-8 col-md-6 col-lg-5 col-xl-4">
        <!-- {% for msg in messages %} {% if 'error' in msg.tags %}
        <div
          class="alert alert-danger d-flex align-items-center col-md-6"
          role="alert"
          style="width: 100% !important; border-radius: 1rem !important"
        >
          <svg
            class="bi flex-shrink-0 me-2"
            width="24"
            height="24"
            role="img"
            aria-label="Danger:"
          >
            <use xlink:href="#exclamation-triangle-fill" />
          </svg>
          <div style="margin-left: 1rem !important">
            {{ msg }}
          </div>
        </div>
        {% endif %} {% endfor %} -->
        <div
          class="bg-secondary rounded p-4"
          style="border-radius: 1rem !important"
        >
          <div
            class="text-center align-items-center justify-content-between mb-4"
          >
            <h3 class="fs-5">Enter new password</h3>
          </div>
          <form method="post" role="form">
            {% csrf_token %}
            <div class="form-floating mb-2">
              <input
                type="password"
                name="new_password1"
                class="form-control form-control-sm"
                style="border-radius: 1rem"
                id="id_new_password1"
                placeholder="Password"
                required
                aria-invalid="true"
              />
              <label for="id_new_password1"
                >Password
                <label style="color: rgb(188, 28, 28)">*</label></label
              >
            </div>
            {{ form.help_text }}
            <div class="form-floating mb-4">
              <input
                type="password"
                name="new_password2"
                class="form-control form-control-sm"
                style="border-radius: 1rem"
                id="id_new_password2"
                placeholder="Password confirmation"
                required
                aria-invalid="true"
              />
              <label for="id_new_password2"
                >Password confirmation
                <label style="color: rgb(188, 28, 28)">*</label></label
              >
            </div>
            {{ form.label }}{{ form.help_text | safe }}
            <button
              type="submit"
              class="btn btn-primary py-3 w-100 mb-2"
              style="border-radius: 1rem !important"
            >
              <label style="color: var(--dark) !important">Submit</label>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import "@/assets/styles/css/bootstrap.min.css";
@import "@/assets/styles/css/style.css";
</style>
