<template>
  <div v-if="!loading" class="profile-view px-5">
    <div class="profile-view__container container-fluid p-0">
      <div class="profile-view__row row">
        <div class="profile-view__sidebar col-3">
          <div
            class="profile-view__meta d-flex flex-column gap-3 p-4 align-items-center"
          >
            <img
              :src="profile.avatar"
              alt="avatar"
              class="profile-view__avatar img-fluid rounded-circle"
              style="width: 10rem; height: 10rem"
            />
            <div
              class="profile-view__username text-primary text-decoration-underline fs-4"
            >
              {{ profile.username }}
            </div>
            <div class="profile-view__bio fs-6 text-light text-center">
              {{ profile.bio }}
            </div>
            <div class="profile-view__tags fs-6 text-light text-center">
              <div
                class="profile-view__tags-list d-flex flex-wrap gap-2 justify-content-center"
              >
                <Tag v-for="tag in profile.tags" :key="tag.id" :tag="tag" />
              </div>
            </div>
            <div
              v-if="profile.telegram || profile.vkontakte"
              class="profile-view__social-links fs-6 text-light text-center d-flex justify-content-center gap-3"
            >
              <a
                v-if="profile.telegram"
                :href="profile.telegram"
                target="_blank"
                class="d-inline-block"
                >Телеграм</a
              >
              <a
                v-if="profile.vkontakte"
                :href="profile.vkontakte"
                target="_blank"
                class="d-inline-block"
                >ВКонтакте</a
              >
            </div>
            <div class="profile-view__stats text-light d-flex gap-4">
              <div class="profile-view__stat d-flex flex-column gap-1">
                <span class="profile-view__stat-field">Посты</span>
                <span>{{ profile.posts.length }}</span>
              </div>
              <div class="profile-view__stat d-flex flex-column gap-1">
                <span class="profile-view__stat-field">Подписчики</span>
                <span>{{ profile.followers.length }}</span>
              </div>
              <div class="profile-view__stat d-flex flex-column gap-1">
                <span class="profile-view__stat-field">Подписки</span>
                <span>{{ profile.following.length }}</span>
              </div>
            </div>
            <div class="profile-view__actions d-flex flex-column gap-2">
              <div class="profile-view__action-buttons d-flex gap-2">
                <button
                  v-if="isAuthenticated"
                  @click="toggleFollow"
                  class="btn btn-action"
                >
                  {{ isFollowing ? "Отписаться" : "Подписаться" }}
                </button>
                <button v-else @click="login" class="btn btn-action">
                  Подписаться
                </button>
                <button class="btn btn-action">Сообщение</button>
              </div>
              <button class="btn btn-action">Пожаловаться</button>
              <router-link
                v-if="isAuthenticated"
                :to="{
                  name: 'profile-edit',
                }"
                class="btn btn-action"
              >
                Редактировать профиль
              </router-link>
              <button class="btn btn-action">Подарок</button>
            </div>
          </div>
        </div>

        <div class="profile-view__content col-9">
          <Tabs
            nav-item-class="profile-view__tab-item nav-item"
            nav-item-active-class="profile-view__tab-item--active nav-item-active"
            nav-item-link-class="profile-view__tab-link nav-item-link"
            nav-class="profile-view__tab-panels-wrapper tab-panels-wrapper"
          >
            <Tab name="Посты">
              <div class="profile-view__posts tab-pane">
                <p
                  v-if="!profile.posts || !profile.posts.length"
                  class="profile-view__no-posts text-secondary fs-7 mt-4 text-center"
                >
                  {{ profile.username }} ничего не публиковал.
                </p>
                <div
                  v-else
                  class="profile-view__posts-list d-flex flex-column gap-3"
                >
                  <Post
                    v-for="post in profile.posts"
                    :key="post.identifier"
                    :post="post"
                  />
                </div>
              </div>
            </Tab>
            <Tab name="Подписчики">
              <div class="profile-view__followers tab-pane">
                <p
                  v-if="!profile.followers || !profile.followers.length"
                  class="profile-view__no-followers text-secondary fs-7 mt-4 text-center"
                >
                  {{ profile.username }} пока никого не подписался.
                </p>
                <div
                  v-else
                  class="profile-view__followers-list d-flex flex-column gap-3"
                >
                  <div
                    v-for="follower in profile.followers"
                    :key="follower.username"
                    class="profile-view__follower-item d-flex align-items-center gap-2"
                  >
                    <img
                      :src="follower.avatar"
                      alt="avatar"
                      class="profile-view__follower-avatar img-fluid rounded-circle"
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
              <div class="profile-view__following tab-pane">
                <p
                  v-if="!profile.following || !profile.following.length"
                  class="profile-view__no-following text-secondary fs-7 mt-4 text-center"
                >
                  {{ profile.username }} пока ни на кого не подписался.
                </p>
                <div
                  v-else
                  class="profile-view__following-list d-flex flex-column gap-3"
                >
                  <div
                    v-for="following in profile.following"
                    :key="following.username"
                    class="profile-view__following-item d-flex align-items-center gap-2"
                  >
                    <img
                      :src="following.avatar"
                      alt="avatar"
                      class="profile-view__following-avatar img-fluid rounded-circle"
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
import Tag from "@/components/Tag.vue";
import { Tabs, Tab } from "vue3-tabs-component";
import { ref, computed, defineProps, onMounted } from "vue";
import ProfileDataService from "@/services/ProfileDataService";
import type ProfileDetailModel from "@/models/ProfileModel";
import type PostListItemModel from "@/models/PostModel";
import { useStore } from "vuex";

const loading = ref(true);

const props = defineProps({
  username: {
    type: String,
    default: "",
  },
});

const store = useStore();

let profile = ref<ProfileDetailModel>(store.getters["profile/getProfile"]);

// TODO: Implement follow/unfollow functionality
const isAuthenticated = ref(true);
const isFollowing = ref(false);

const toggleFollow = () => {
  isFollowing.value = !isFollowing.value;
};

const login = () => {
  console.log("Redirect to login");
};

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
  /* border-top-left-radius: 0.4rem !important;
  border-top-right-radius: 0.4rem !important; */
  border-radius: 0.4rem !important;
  padding: 0.5rem 1rem;
  font-weight: 700;
}

.nav-item:hover {
  color: var(--light) !important;
}

.nav-item-active {
  border-bottom: 1px solid var(--primary);
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
  /* border-bottom: 1px solid var(--secondary); */
}
</style>

<style scoped>
.profile-view__container {
  border-radius: 0.4rem;
}

/* .profile-view__meta {
  border-top-left-radius: 0.4rem;
  border-bottom-left-radius: 0.4rem;
} */

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

.profile-view__stat {
  color: var(--secondary-xx-light);
}

.field {
  font-weight: bold;
}

#posts-nav button.active {
  border-bottom: 1px solid var(--secondary-x-light);
}
</style>
