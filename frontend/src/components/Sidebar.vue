<template>
  <div
    class="sidebar pe-0 pb-3 border border-2 open"
    style="
      border-right: 0.1px solid var(--secondary) !important;
      background-color: var(--dark) !important;
    "
  >
    <nav
      id="sidebar-nav"
      class="navbar bg-secondary navbar-dark align-items-center"
      style="background-color: var(--dark) !important"
    >
      <p
        class="text-break fs-9 w-100 p-3 pt-0 pb-0"
        style="color: var(--secondary-light)"
      >
        What's the rush?
        <br />
        Just relax and enjoy another hour of free studying with
        <em>Tell Your Friends!</em>
      </p>
      <!-- TODO: ADD id="search-input" -->
      <input
        id="termin-search"
        type="text"
        class="form-control bg-transparent border-0 mb-4 ms-3 me-4"
        placeholder="Search..."
        style="
          border: 0.1px solid var(--primary) !important;
          border-top: 0 !important;
          border-left: 0 !important;
          border-right: 0;
          padding-right: 0;
          color: var(--light) !important;
          padding-left: 0.5em;
          font-weight: 100 !important;
          font-size: smaller !important;
          border-radius: 0.2em;
          box-shadow: none !important;
        "
      />
      <div class="navbar-nav ps-3 w-100">
        <div class="nav-item dropdown">
          <a
            href="#"
            class="nav-link dropdown-toggle fs-6"
            data-bs-toggle="dropdown"
            >📚 Collections</a
          >
          <div
            id="collections"
            class="dropdown-menu bg-transparent border-0 pt-0"
          >
            {% for collection in collections %}
            <a
              href="#"
              onclick="collection_help('{{ collection }}')"
              class="dropdown-item fs-7"
              style="display: block !important"
              >{{ collection }}</a
            >
            {% endfor %}
          </div>
        </div>
        <div class="nav-item dropdown">
          <a
            href="#"
            class="nav-link dropdown-toggle fs-6"
            data-bs-toggle="dropdown"
            >📁 Categories</a
          >
          <div
            id="categories"
            class="dropdown-menu bg-transparent border-0 pt-0"
          >
            {% for category in categories %}
            <a
              href="#"
              onclick="category_help('{{ category }}')"
              class="dropdown-item fs-7"
              style="display: block !important"
              >{{ category }}</a
            >
            {% endfor %}
          </div>
        </div>
        <div class="nav-item dropdown">
          <a
            href="#"
            class="nav-link dropdown-toggle fs-6"
            data-bs-toggle="dropdown"
            >🔖 Tags</a
          >
          <div id="tags" class="dropdown-menu bg-transparent border-0 pt-0">
            <div class="px-3">
              {% for tag in tags %} {% include 'main/tag.html' with tag=tag %}
              {% endfor %}
            </div>
          </div>
        </div>
      </div>
    </nav>
    <div>
      <a href="https://github.com/EmotionlessDev/tyf" class="dropdown-item"
        >⭐ Support Us</a
      >
      <a
        href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        class="dropdown-item"
        >🛠️ Report a bug</a
      >
    </div>
  </div>
</template>
