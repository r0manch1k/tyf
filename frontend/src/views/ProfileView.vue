<template>
  <div v-if="!loading">
    <div class="p-5">
      <div class="row">
        <!-- Profile -->
        <div class="col-md-3 text-center">
          <img
            :src="profile.avatar"
            alt="avatar"
            class="img-fluid rounded-circle"
          />
          <p class="mt-3 fs-4 text-break">{{ profile.username }}</p>
          <div class="action-buttons">
            <button
              v-if="isAuthenticated"
              class="btn btn-outline-primary w-100 mt-2"
              :class="isFollowing ? 'action-checked' : 'action-unchecked'"
              @click="toggleFollow"
            >
              {{ isFollowing ? "Отписаться" : "Подписаться" }}
            </button>
            <button
              v-else
              class="btn btn-outline-primary w-100 mt-2 action-unchecked"
              @click="login"
            >
              Подписаться
            </button>
          </div>
          <hr class="mt-3" />
          <ul class="list-unstyled d-flex flex-column fs-7">
            <li>
              <div class="d-flex align-items-center gap-1 mb-0">
                <span class="badge bg-secondary">{{ profile.points }}</span>
                Очки
              </div>
            </li>
            <li>
              <div class="d-flex align-items-center gap-1 mb-0">
                <span class="badge bg-secondary">{{ profile.awards }}</span>
                Награды
              </div>
            </li>
          </ul>
        </div>

        <!-- Tabs -->
        <div class="col-md-9 fs-7">
          <Tabs
            nav-item-class="nav-item"
            nav-item-active-class="nav-item-active"
            nav-item-link-class="nav-item-link"
            nav-class="tab-panels-wrapper"
          >
            <Tab name="Общее" :selected="true">
              <div class="mt-4 text-start">
                <p v-if="profile.bio">
                  <em class="about-field">О себе: </em>{{ profile.bio }}
                </p>
                <p v-if="profile.email">
                  <em class="about-field">Почта: </em>{{ profile.email }}
                </p>
                <p v-if="profile.date_of_birth">
                  <em class="about-field">Дата рождения: </em
                  >{{ profile.date_of_birth }}
                </p>
                <p v-if="profile.date_joined">
                  <em class="about-field">Дата регистрации: </em
                  >{{ new Date(profile.date_joined).toLocaleDateString() }}
                </p>
                <p v-if="profile.university">
                  <em class="about-field">Университет: </em
                  >{{ profile.university }}
                </p>
                <p v-if="profile.major">
                  <em class="about-field">Напрваление: </em>{{ profile.major }}
                </p>
              </div>
            </Tab>
            <Tab name="Посты">
              <div class="tab-pane">
                <p
                  v-if="!profile.posts || !profile.posts.length"
                  class="text-secondary fs-7 mt-4 text-center"
                >
                  {{ profile.username }} ничего не публиковал.
                </p>
                <ul v-else>
                  <li v-for="post in profile.posts" :key="post.id">
                    {{ post.content }}
                  </li>
                </ul>
              </div>
            </Tab>
          </Tabs>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <LoadingCircle />
  </div>
</template>

<script setup lang="ts">
import LoadingCircle from "@/components/LoadingCircle.vue";
import { ref, computed, defineProps, onMounted } from "vue";
import { useStore } from "vuex";

const loading = ref(true);

const props = defineProps({
  username: String,
});

const store = useStore();

const profile = computed(() => {
  console.log("Getting profile", props.username);
  return store.getters["profile/getProfileByUsername"](props.username);
});

// TODO: Implement follow/unfollow functionality
const isAuthenticated = ref(true);
const isFollowing = ref(false);

const toggleFollow = () => {
  isFollowing.value = !isFollowing.value;
};

const login = () => {
  console.log("Redirect to login");
};

// TODO: Fix header dissapearing on profile page load
onMounted(async () => {
  await store.dispatch("profile/fetchProfileByUsername", props.username);
  loading.value = false;
});
</script>

<style>
.nav-item {
  width: 100%;
  display: block;
  border: none;
  border-bottom: 1px solid var(--secondary);
  background: none;
  padding: 0.5rem 1rem;
  font-weight: 500;
}

.nav-item-active {
  border-bottom: 1px solid var(--primary);
}

.nav-item-link {
  display: flex;
  justify-content: center;
  color: var(--light);
}

.tab-panels-wrapper {
  display: flex;
}
</style>

<style scoped>
/* BUTTONS */

.action-checked:focus,
.action-unchecked:focus {
  outline: none !important;
  box-shadow: none !important;
}

.action-unchecked,
.action-checked:hover {
  color: var(--light);
  background-color: var(--dark);
  font-size: smaller;
  outline: none !important;
  box-shadow: none;
}

.action-checked,
.action-unchecked:hover {
  color: var(--dark);
  background-color: var(--primary);
  border-right: 1px solid var(--light);
  border-bottom: 1px solid var(--light);
  font-size: smaller;
  outline: none !important;
  box-shadow: none;
}

.avatars-block {
  display: inline-flex;
}

.avatar {
  width: 1.6em;
  height: 1.6em;
  border-radius: 50%;
  border: 2px solid var(--dark);
}

.avatar-bigger {
  width: 4em;
  height: 4em;
  border-radius: 50%;
  border: 2px solid var(--dark);
}

.reduce-margin-right {
  margin-right: -0.5em;
}

.about-field {
  color: var(--secondary-xx-light);
  font-weight: 100;
  /* text-decoration: underline;
    text-decoration-color: var(--primary);
    text-decoration-thickness: 0.01em; */
}

#posts-nav button.active {
  border-bottom: 1px solid var(--secondary-x-light);
}
</style>
