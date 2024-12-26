<template>
  <!-- <nav
    class="navbar navbar-expand bg-secondary navbar-dark sticky-top px-4 py-0"
    style="
      background-color: var(--dark) !important;
      border-bottom: 0.1px solid var(--secondary) !important;
    "
  >
    <a href="{% url 'index' %}" class="navbar-brand d-flex me-4">
      <img
        class=""
        src="{% static 'img/logo.svg' %}"
        alt=""
        style="height: 35px"
      />
    </a>
    <a href="#" class="sidebar-toggler flex-shrink-0">
      <i class="bi bi-list fs-4 text-light"></i>
    </a>
    <div class="ms-4 w-100">
      <input
        id="search-input"
        class="js-typing-color form-control fs-7 bg-dark border-0"
        type="search"
        placeholder="Search"
      />
    </div>
    <a
      href="{% url 'post_add' %}"
      class="btn btn-outline-primary fs-8 ms-4 action-super"
      >+ Create</a
    >
    <div class="navbar-nav align-items-center ms-0">
      <div class="nav-item dropdown">
        // TODO: Add image
        <router-link
          :to="{ name: 'profile', params: { username: 'string' } }"
          class="nav-link dropdown-toggle ms-0"
          data-bs-toggle="dropdown"
        >
        </router-link>

        <a
          href="{% url 'login' %}"
          class="nav-link dropdown-toggle"
          data-bs-toggle="dropdown"
        >
          <img
            class="rounded-circle me-lg-0"
            src="{% static 'img/default_avatar.webp' %}"
            alt=""
            style="width: 30px; height: 30px"
          />
        </a>
        {% endif %}
        <div
          class="dropdown-menu dropdown-menu-end bg-dark border-secondary border-top-0 rounded-0 rounded-bottom fs-8"
        >
          {% if user.is_authenticated %}
          <a
            href="{% url 'profile' username=request.user.profile.username %}"
            class="dropdown-item"
            >Profile</a
          >
          {% endif %} {% if user.is_authenticated %}
          <a href="{% url 'logout' %}" class="dropdown-item">Log Out</a>
          {% else %}
          <a href="{% url 'login' %}" class="dropdown-item">Log In</a>
          {% endif %}
        </div>
      </div>
    </div>
  </nav> -->
  <p style="color: white">FKLDJSKLFJSDKLJFKLSDJFJSDKLJFKDJFKLjskldj</p>
  <router-link
    :to="{ name: 'profile', params: { username: 'contentBustard2' } }"
    class="nav-link dropdown-toggle ms-0"
    data-bs-toggle="dropdown"
  >
  </router-link>
</template>
