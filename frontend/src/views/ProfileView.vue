<template>
  <div v-if="!loading" class="profile-view px-5">
    <div class="profile-view__container container-fluid p-0">
      <div class="profile-view__row row">
        <div class="profile-view__sidebar col-3">
          <div
            class="profile-view__meta-container d-flex flex-column gap-3 p-3"
          >
            <img
              :src="profile.avatar"
              alt="avatar"
              class="profile-view__avatar img-fluid rounded-circle"
              style="width: max-content; height: max-content"
            />
            <div class="profile-view__username text-primary w-100 fs-3">
              {{ profile.username }}
            </div>
            <div class="profile-view__actions d-flex flex-column w-100 gap-2">
              <button
                v-if="isAuth && guestMode"
                @click="toggleFollow"
                class="btn btn-action text-decoration-none text-light"
                :class="{
                  'action-checked': profile.is_followed_by_request_user,
                  'action-unchecked': !profile.is_followed_by_request_user,
                }"
                :disabled="loadingToggleFollow"
              >
                <span v-if="!loadingToggleFollow">
                  {{
                    profile.is_followed_by_request_user
                      ? "Отписаться"
                      : "Подписаться"
                  }}
                </span>
                <LoadingCircle v-else class="spinner-border-sm" />
              </button>

              <router-link
                v-if="isAuth && !guestMode"
                :to="{
                  name: 'profile-edit',
                }"
                class="btn btn-action text-decoration-none text-light"
              >
                Редактировать профиль
              </router-link>
            </div>
            <div class="profile-view__meta d-flex flex-column gap-1">
              <div
                class="profile-view__name fs-6 text-secondary-xx-light w-100 text-start"
                v-if="
                  profile.first_name || profile.last_name || profile.middle_name
                "
              >
                <p class="fw-bold text-decoration-underline">Имя:</p>
                <div class="d-flex gap-2">
                  <span v-if="profile.first_name">{{
                    profile.first_name
                  }}</span>
                  <span v-if="profile.last_name">{{ profile.last_name }}</span>
                  <span v-if="profile.middle_name">{{
                    profile.middle_name
                  }}</span>
                </div>
              </div>
              <div
                class="profile-view__bio fs-6 text-secondary-xx-light w-100 text-start"
                v-if="profile.bio"
              >
                <p class="fw-bold text-decoration-underline">О себе:</p>
                <p>{{ profile.bio }}</p>
              </div>
              <div
                class="profile-view__stat fs-6 text-secondary-xx-light w-100 text-start"
                v-if="profile.university"
              >
                <p class="fw-bold text-decoration-underline">Университет:</p>
                <p>
                  {{
                    profile.university.name +
                    " (" +
                    profile.university.city +
                    ", " +
                    profile.university.country +
                    ")"
                  }}
                </p>
              </div>
              <div
                class="profile-view__stat fs-6 text-secondary-xx-light w-100 text-start"
                v-if="profile.major"
              >
                <p class="fw-bold text-decoration-underline">Направление:</p>
                <p>
                  {{ profile.major.name + " (" + profile.major.code + ")" }}
                </p>
              </div>

              <div class="profile-view__links fs-6 text-light w-100 text-start">
                <div class="profile-view__links-list d-flex flex-wrap gap-2">
                  <div
                    class="profile-view__link-item d-flex gap-2"
                    v-if="profile.email"
                  >
                    <p class="fw-bold text-decoration-underline">Email:</p>
                    <span>
                      <a
                        v-if="profile.email"
                        :href="'mailto:' + profile.email"
                        class="d-inline-block text-decoration-none"
                        >{{ profile.email }}</a
                      >
                    </span>
                  </div>
                  <div
                    class="profile-view__link-item d-flex gap-2"
                    v-if="profile.telegram"
                  >
                    <p class="fw-bold text-decoration-underline">Телеграм:</p>
                    <span>
                      <a
                        v-if="profile.telegram"
                        :href="profile.telegram"
                        class="d-inline-block text-decoration-none"
                        >{{ profile.telegram_alias }}</a
                      >
                    </span>
                  </div>

                  <div
                    class="profile-view__link-item d-flex gap-2"
                    v-if="profile.vkontakte"
                  >
                    <p class="fw-bold text-decoration-underline">ВКонтакте:</p>
                    <span>
                      <a
                        v-if="profile.vkontakte"
                        :href="profile.vkontakte"
                        class="d-inline-block text-decoration-none"
                        >{{ profile.vkontakte_alias }}</a
                      >
                    </span>
                  </div>
                </div>
              </div>
              <!-- <div
                class="profile-view__date-joined fs-6 text-secondary-xx-light w-100 text-start d-flex gap-2 flex-wrap"
              >
                <p class="fw-bold text-decoration-underline">
                  Дата регистрации:
                </p>
                <p>{{ profile.date_joined }}</p>
              </div> -->
              <!-- <div
                class="profile-view__date-of-birth fs-6 text-secondary-xx-light w-100 text-start d-flex gap-2"
              >
                <p class="fw-bold text-decoration-underline">Дата рождения:</p>
                <p>{{ profile.date_of_birth }}</p>
              </div> -->
              <div
                class="profile-view__tags fs-6 text-secondary-xx-light w-100 text-start"
                v-if="profile.tags && profile.tags.length > 0"
              >
                <p class="fw-bold text-decoration-underline">Избранные теги:</p>
                <div class="d-flex gap-2 fs-6 mt-1">
                  <Tag v-for="tag in profile.tags" :key="tag.id" :tag="tag" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="profile-view__content col-9 pt-3">
          <Tabs
            nav-item-class="profile-view__tab-item nav-item"
            nav-item-active-class="profile-view__tab-item--active nav-item-active"
            nav-item-link-class="profile-view__tab-link nav-item-link"
            nav-class="profile-view__tab-panels-wrapper tab-panels-wrapper"
            @changed="onTabChanged"
          >
            <Tab :name="`Публикации(${profile.posts_count})`">
              <div class="profile-view__posts tab-pane" v-if="!loadingPosts">
                <p
                  v-if="!profile.posts || !profile.posts.length"
                  class="profile-view__no-posts text-secondary-light fs-6 mt-4 text-start"
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
              <LoadingCircle v-else />
            </Tab>
            <Tab :name="`Подписчики(${profile.followers_count})`">
              <div
                class="profile-view__followers tab-pane"
                v-if="!loadingFollowers"
              >
                <p
                  v-if="!profile.followers || !profile.followers.length"
                  class="profile-view__no-followers text-secondary-light fs-6 mt-4 text-start"
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
                    <ProfileListItemLarge :profile="follower" />
                  </div>
                </div>
              </div>
              <LoadingCircle v-else />
            </Tab>
            <Tab :name="`Подписки(${profile.following_count})`">
              <div
                class="profile-view__following tab-pane"
                v-if="!loadingFollowing"
              >
                <p
                  v-if="!profile.following || !profile.following.length"
                  class="profile-view__no-following text-secondary-light fs-6 mt-4 text-start"
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
                    <ProfileListItemLarge :profile="following" />
                  </div>
                </div>
              </div>
              <LoadingCircle v-else />
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
import { ref, defineProps, onMounted, computed, watch } from "vue";
import { useStore } from "vuex";
import { Tabs, Tab } from "vue3-tabs-component";
import LoadingCircle from "@/components/LoadingCircle.vue";
import ProfileListItemLarge from "@/components/ProfileListItemLarge.vue";
import Post from "@/components/Post.vue";
import Tag from "@/components/Tag.vue";
import type { ProfileDetailModel } from "@/models/ProfileModel";
import ProfileDataService from "@/services/ProfileDataService";

const store = useStore();

const loading = ref(true);
const loadingPosts = ref(true);
const loadingFollowers = ref(true);
const loadingFollowing = ref(true);
const loadingToggleFollow = ref(false);

const props = defineProps({
  username: {
    type: String,
    default: "",
  },
});

watch(
  () => props.username,
  async () => {
    await fetchProfile();
  }
);

const profile = ref<ProfileDetailModel>(store.getters["profile/getProfile"]);
const isAuth = computed(() => profile.value.id > -1);
const guestMode = computed(
  () => store.getters["profile/getProfile"].username != props.username
);

onMounted(async () => {
  await fetchProfile();
});

const fetchProfile = async () => {
  loading.value = true;
  loadingPosts.value = true;
  loadingFollowers.value = true;
  loadingFollowing.value = true;

  await ProfileDataService.getProfileByUsername(props.username).then(
    (response) => {
      profile.value = response;
      loading.value = false;
    }
  );
};

const fetchPosts = async () => {
  if (profile.value.posts) {
    return;
  }
  loadingPosts.value = true;
  await ProfileDataService.getProfilePosts(props.username).then((response) => {
    profile.value.posts = response;
    loadingPosts.value = false;
  });
};

const fetchFollowers = async () => {
  if (profile.value.followers) {
    return;
  }
  loadingFollowers.value = true;
  await ProfileDataService.getProfileFollowers(props.username).then(
    (response) => {
      profile.value.followers = response;
      loadingFollowers.value = false;
    }
  );
};

const fetchFollowing = async () => {
  if (profile.value.following) {
    return;
  }
  loadingFollowing.value = true;
  await ProfileDataService.getProfileFollowing(props.username).then(
    (response) => {
      profile.value.following = response;
      loadingFollowing.value = false;
    }
  );
};

interface TabObject {
  tab: {
    name: string;
    header: string;
    isDisabled: boolean;
  };
}

const onTabChanged = (object: TabObject) => {
  if (object.tab.name.includes("Публикации")) {
    fetchPosts();
  } else if (object.tab.name.includes("Подписчики")) {
    fetchFollowers();
  } else if (object.tab.name.includes("Подписки")) {
    fetchFollowing();
  }
};

const toggleFollow = async () => {
  loadingToggleFollow.value = true;
  if (isAuth.value && guestMode) {
    await ProfileDataService.followProfile(props.username);
  }
  loadingToggleFollow.value = false;
  await fetchProfile();
};
</script>

<style>
ul {
  padding-left: 0 !important;
}

.nav-item {
  display: block;
  color: var(--light);
  /* border-bottom: 1px solid var(--secondary); */
  border-top-left-radius: 0.4rem !important;
  border-top-right-radius: 0.4rem !important;
  /* padding: 0.5rem 1rem; */
}

.nav-item:hover {
  color: var(--light) !important;
}

.nav-item-active {
  /* border-bottom: 1px solid var(--primary); */
  text-decoration: underline;
  text-decoration-color: var(--primary);
}

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
/* .profile-view__avatar {
  border: 1px solid var(--secondary);
} */

.profile-view__container {
  border-radius: 0.4rem;
}

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
  color: var(--secondary-xx-light);
}
</style>
