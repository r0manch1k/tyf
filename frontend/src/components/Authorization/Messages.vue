<template>
  {% for msg in messages %} {% if 'success' in msg.tags %}
  <div
    class="alert alert-success d-flex align-items-center"
    role="alert"
    style="width: 100% !important; border-radius: 1rem !important"
  >
    <svg
      class="bi flex-shrink-0 me-2"
      width="24"
      height="24"
      role="img"
      aria-label="Success:"
    >
      <use xlink:href="#check-circle-fill" />
    </svg>
    <div style="margin-left: 1rem !important">
      {{ msg }}
    </div>
  </div>
  {% endif %} {% if 'info' in msg.tags %}
  <div
    class="alert alert-info d-flex align-items-center"
    role="alert"
    style="width: 100% !important; border-radius: 1rem !important"
  >
    <svg
      class="bi flex-shrink-0 me-2"
      width="24"
      height="24"
      role="img"
      aria-label="Warning:"
    >
      <use xlink:href="#info-fill" />
    </svg>
    <div style="margin-left: 1rem !important">
      {{ msg }}
    </div>
  </div>
  {% endif %} {% if 'warning' in msg.tags %}
  <div
    class="alert alert-warning d-flex align-items-center"
    role="alert"
    style="width: 100% !important; border-radius: 1rem !important"
  >
    <svg
      class="bi flex-shrink-0 me-2"
      width="24"
      height="24"
      role="img"
      aria-label="Warning:"
    >
      <use xlink:href="#exclamation-triangle-fill" />
    </svg>
    <div style="margin-left: 1rem !important">
      {{ msg }}
    </div>
  </div>
  {% endif %} {% if 'error' in msg.tags %}
  <div
    class="alert alert-danger d-flex align-items-center"
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
  {% endif %} {% endfor %}
</template>
