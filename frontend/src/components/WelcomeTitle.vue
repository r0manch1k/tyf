<template>
  <div>
    <div class="w-100 mb-0 main__content container">
      <div class="main_background"></div>
      <div class="row position-relative px-4">
        {% block content %}
        <div id="greetings">
          <h1 class="mt-4 h1-super color-light fs-0">
            Welcome To
            <span class="color-primary">Tell Your Friends</span>
            <span>!</span>
          </h1>
          <h2 class="fs-6 text-light mt-3" style="font-weight: 300">
            <em>
              You've arrived in a space where the noise of the world fades, and
              the whispers of your potential take center stage. Open the door to
              a realm where your thoughts transform into a beacon for others, a
              sanctuary where students exchange more than notes—they exchange
              purpose.
              <br /><br />
              Among these pages, you'll find collaborators, dreamers, seekers of
              the same light you carry. Share your work, gather a team, or plant
              the seeds of something extraordinary. This isn't just a platform,
              it's a reflection of what you can become when you choose to
              inspire and be inspired.
              <br /><br />
              So leave your mark. Because here on
              <strong style="font-weight: 800">Tell Your Friends</strong>, your
              voice doesn't just echo — it resonates forever.
            </em>
          </h2>
          <hr class="my-4" />
        </div>
        <div id="search-container" class="fs-9"></div>
        <div class="col-9">
          <div id="posts"></div>
        </div>
        <div class="col-3" id="recent-users">
          <div class="card bg-dark p-2 mt-0">
            <p class="text-light text-center m-0 mt-1 fs-9>">Recent Users</p>
            <hr class="mt-2 mb-3" />
            {% for profile in recent_users %}
            <div class="d-flex align-items-center gap-2 mb-3">
              <!-- TODO: Fix this -->
              <!-- <a href="{% url 'profile' username=profile.username %}">
                <img
                  src="{{ profile.get_avatar }}"
                  alt="avatar"
                  class="img-fluid rounded-circle"
                  style="width: 40px; height: 40px"
                />
              </a>
              <div class="d-flex flex-column gap-1">
                <a href="{% url 'profile' username=profile.username %}">
                  <p class="m-0 p-0 fs-9">{{ profile.username }}</p>
                </a>
                <p class="m-0 p-0 fs-9">Since {{ profile.date_joined }}</p>
              </div> -->
            </div>
            {% endfor %}
          </div>
        </div>
        <div
          class="p-4 pb-0 w-100 text-center mb-3"
          style="color: var(--secondary-light)"
        >
          <hr />
          <a
            href="{% url 'index' %}"
            class="fs-9"
            style="color: var(--secondary-light)"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-arrow-clockwise"
              viewBox="0 0 16 16"
            >
              <path
                fill-rule="evenodd"
                d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2z"
              />
              <path
                d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466"
              />
            </svg>
            Reload the page to refresh post feed
          </a>
        </div>
        {% endblock %}
      </div>
    </div>
  </div>
</template>
