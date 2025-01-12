<template>
  <div v-if="!loading">
    <div class="px-5 py-4">
      <div class="row">
        <div class="col-md-3 text-center pt-6">
          <img
            :src="profile.avatar"
            alt="avatar"
            class="img-fluid rounded-circle"
            style="width: 15rem; height: 15rem"
          />
          <h1 class="fs-3 mt-3 text-light">{{ profile.username }}</h1>
          <div class="action-buttons fs-5">
            <button
              v-if="isAuthenticated"
              class="btn-light mt-2"
              @click="toggleFollow"
            >
              {{ isFollowing ? "Отписаться" : "Подписаться" }}
            </button>
            <button v-else class="btn-light" @click="login">Подписаться</button>
          </div>
          <hr class="mt-3" />
          <!-- <ul class="list-unstyled d-flex flex-column fs-7">
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
          </ul> -->
        </div>

        <div class="col-md-9">
          <Tabs
            nav-item-class="nav-item"
            nav-item-active-class="nav-item-active"
            nav-item-link-class="nav-item-link"
            nav-class="tab-panels-wrapper"
          >
            <Tab name="Информация" :selected="true">
              <div class="card bg-dark-light text-start">
                <!-- <div class="card-header">
                  <h2 class="fs-5 text-light fw-normal mb-0">
                    Информация о пользователе
                    {{ profile.username }}
                  </h2>
                </div> -->
                <div class="card-body d-flex flex-column gap-2 fs-6 pt-3 pb-3">
                  <p v-if="profile.first_name">
                    <span class="field">Имя: </span>{{ profile.first_name }}
                  </p>
                  <p v-if="profile.last_name">
                    <span class="field">Фамилия: </span>{{ profile.last_name }}
                  </p>
                  <p v-if="profile.middle_name">
                    <span class="field">Отчество: </span
                    >{{ profile.middle_name }}
                  </p>
                  <p v-if="profile.username">
                    <span class="field">Имя пользователя: </span
                    >{{ profile.username }}
                  </p>
                  <p v-if="profile.email">
                    <span class="field">Почта: </span>{{ profile.email }}
                  </p>
                  <p v-if="profile.date_of_birth">
                    <span class="field">Дата рождения: </span
                    >{{ new Date(profile.date_of_birth).toLocaleDateString() }}
                  </p>
                  <p v-if="profile.date_joined">
                    <span class="field">Дата регистрации: </span
                    >{{ new Date(profile.date_joined).toLocaleDateString() }}
                  </p>
                  <p v-if="profile.university">
                    <span class="field">Университет: </span
                    >{{ profile.university.name }}
                  </p>
                  <p v-if="profile.major">
                    <span class="field">Направление : </span
                    >{{ profile.major.name + " (" + profile.major.code + ")" }}
                  </p>
                  <p v-if="profile.bio">
                    <span class="field">О себе: </span>{{ profile.bio }}
                  </p>
                  <div
                    v-if="profile.telegram"
                    class="d-flex align-items-center gap-1"
                  >
                    <span class="field">Telegram: </span>
                    <a :href="profile.telegram">{{ profile.telegram }}</a>
                  </div>
                  <div
                    v-if="profile.vkontakte"
                    class="d-flex align-items-center gap-1"
                  >
                    <span class="field">VK: </span>
                    <a :href="profile.vkontakte">{{ profile.vkontakte }}</a>
                  </div>
                </div>
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
                <div v-else class="d-flex flex-column gap-3">
                  <Post
                    v-for="post in profile.posts"
                    :key="post.identifier"
                    :post="post"
                  />
                </div>
              </div>
            </Tab>
            <Tab name="Подписчики">
              <div class="tab-pane">
                <p
                  v-if="!profile.followers || !profile.followers.length"
                  class="text-secondary fs-7 mt-4 text-center"
                >
                  {{ profile.username }} пока никого не подписался.
                </p>
                <div v-else class="d-flex flex-column gap-3">
                  <div
                    v-for="follower in profile.followers"
                    :key="follower.username"
                    class="d-flex align-items-center gap-2"
                  >
                    <img
                      :src="follower.avatar"
                      alt="avatar"
                      class="img-fluid rounded-circle"
                      style="width: 3rem; height: 3rem"
                    />
                    <div>
                      <a :href="'/profile/' + follower.username">
                        {{ follower.username }}
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </Tab>
            <Tab name="Подписки">
              <div class="tab-pane">
                <p
                  v-if="!profile.following || !profile.following.length"
                  class="text-secondary fs-7 mt-4 text-center"
                >
                  {{ profile.username }} пока ни на кого не подписался.
                </p>
                <div v-else class="d-flex flex-column gap-3">
                  <div
                    v-for="following in profile.following"
                    :key="following.username"
                    class="d-flex align-items-center gap-2"
                  >
                    <img
                      :src="following.avatar"
                      alt="avatar"
                      class="img-fluid rounded-circle"
                      style="width: 3rem; height: 3rem"
                    />
                    <div>
                      <a :href="'/profile/' + following.username">
                        {{ following.username }}
                      </a>
                    </div>
                  </div>
                </div>
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
import Post from "@/components/Post.vue";
import { Tabs, Tab } from "vue3-tabs-component";
import { ref, defineProps, onMounted } from "vue";
// import { computed } from "vue";
import ProfileDataService from "@/services/ProfileDataService";
import type ProfileDetailModel from "@/models/ProfileModel";
// import type PostListItemModel from "@/models/PostModel";
import { useStore } from "vuex";

const loading = ref(true)

const props = defineProps({
  username: {
    type: String,
    default: "",
  },
});

const store = useStore()

let profile = ref<ProfileDetailModel>(store.getters["profile/getProfile"]);

// TODO: Implement follow/unfollow functionality
const isAuthenticated = ref(true)
const isFollowing = ref(false)

const toggleFollow = () => {
	isFollowing.value = !isFollowing.value
}

const login = () => {
	console.log('Redirect to login')
}

onMounted(async () => {
  await Promise.all([
    (profile.value = await ProfileDataService.getProfileByUsername(
      props.username
    )),
    (profile.value.posts = await ProfileDataService.getProfilePosts(
      props.username
    )),
  ]).then(() => {
    loading.value = false;
  });
});
</script>

<style>
ul {
  padding-left: 0 !important;
}

.nav-item {
  width: 100%;
  display: block;
  background-color: var(--dark-light);
  color: var(--light);
  border-radius: 0.4rem !important;
  padding: 0.5rem 1rem;
  font-weight: 700;
}

.nav-item:hover {
  color: var(--light) !important;
}

.nav-item-active {
  background-color: var(--secondary);
  color: var(--dark-light);
}

/* .nav-item-active:hover {
  color: var(--dark-light);
}

.nav-item-link.is-active {
  color: var(--dark-light);
}

.nav-item-link.is-active:hover {
  color: var(--dark-light);
} */

.nav-item-link {
	display: flex;
	justify-content: center;
	color: var(--light);
}

.tab-panels-wrapper {
  display: flex;
  gap: 1rem;
}
</style>

<style scoped>
<<<<<<< HEAD
a {
  color: var(--primary);
  text-decoration: underline;
}

a:hover {
  color: var(--primary);
}

p {
  color: var(--secondary-xx-light);
  margin: 0;
}

.field {
  font-weight: bold;
  color: var(--secondary-xx-light);
=======
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
>>>>>>> 7-authorization-system
}

#posts-nav button.active {
	border-bottom: 1px solid var(--secondary-x-light);
}
</style>
