<template>
  <div v-if="!loading" class="profile-view px-5">
    <div class="profile-view__container container-fluid p-0">
      <div class="profile-view__row row">
        <div class="profile-view__sidebar col-md-3">
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
                v-if="guestMode"
                @click="toggleFollow"
                class="btn btn-action text-decoration-none text-light"
                :class="{
                  'action-checked': profile.is_followed_by_request_user,
                  'action-unchecked': !profile.is_followed_by_request_user,
                }"
                :disabled="loadingToggleFollow || loadingProfile"
              >
                <span v-if="!loadingToggleFollow && !loadingProfile">
                  {{
                    profile.is_followed_by_request_user
                      ? "Отписаться"
                      : "Подписаться"
                  }}
                </span>
                <LoadingCircle
                  v-else
                  class="spinner-border-sm mx-auto my-auto"
                />
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

              <button
                v-if="isAuth && guestMode"
                @click="sendMessage"
                class="btn btn-action text-decoration-none text-light"
                :disabled="loadingSendMesssage"
              >
                <span v-if="!loadingSendMesssage">Написать сообщение</span>
                <LoadingCircle
                  v-else
                  class="spinner-border-sm mx-auto my-auto"
                />
              </button>
            </div>
            <div
              class="profile-view__meta d-flex flex-column text-light gap-1 text-start"
            >
              <div
                class="profile-view__name fs-6 text-light w-100 text-start"
                v-if="
                  profile.first_name || profile.last_name || profile.middle_name
                "
              >
                <p class="profile-view__stat-label">Имя:</p>
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
                class="profile-view__bio fs-6 text-light w-100 text-start"
                v-if="profile.bio"
              >
                <p class="profile-view__stat-label">О себе:</p>
                <p>{{ profile.bio }}</p>
              </div>
              <div
                class="profile-view__stat fs-6 text-light w-100 text-start"
                v-if="profile.university"
              >
                <p class="profile-view__stat-label">Университет:</p>
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
                class="profile-view__stat fs-6 text-light w-100 text-start"
                v-if="profile.major"
              >
                <p class="profile-view__stat-label">Направление:</p>
                <p>
                  {{ profile.major.name + " (" + profile.major.code + ")" }}
                </p>
              </div>

              <div class="profile-view__links fs-6 text-light w-100 text-start">
                <div class="profile-view__links-list d-flex flex-wrap gap-2">
                  <div
                    class="profile-view__stat fs-6 text-light w-100 text-start"
                    v-if="profile.email"
                  >
                    <p class="profile-view__stat-label">Email:</p>
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
                    class="profile-view__stat fs-6 text-light w-100 text-start"
                    v-if="profile.telegram"
                  >
                    <p class="profile-view__stat-label">Телеграм:</p>
                    <span>
                      <a
                        v-if="profile.telegram"
                        :href="profile.telegram"
                        target="_blank"
                        class="d-inline-block text-decoration-none"
                        >{{ profile.telegram_alias }}</a
                      >
                    </span>
                  </div>

                  <div
                    class="profile-view__stat fs-6 text-light w-100 text-start"
                    v-if="profile.vkontakte"
                  >
                    <p class="profile-view__stat-label">ВКонтакте:</p>
                    <span>
                      <a
                        v-if="profile.vkontakte"
                        :href="profile.vkontakte"
                        target="_blank"
                        class="d-inline-block text-decoration-none"
                        >{{ profile.vkontakte_alias }}</a
                      >
                    </span>
                  </div>
                </div>
              </div>
              <div
                class="profile-view__date-joined s-6 text-light w-100 text-start"
              >
                <p class="profile-view__stat-label">Дата регистрации:</p>
                <p>{{ profile.date_joined }}</p>
              </div>
              <!-- <div
                class="profile-view__date-of-birth fs-6 text-secondary-xx-light w-100 text-start d-flex gap-2"
              >
                <p class="fw-bold text-decoration-underline">Дата рождения:</p>
                <p>{{ profile.date_of_birth }}</p>
              </div> -->
              <div
                class="profile-view__tags fs-6 text-light w-100 text-start"
                v-if="profile.tags && profile.tags.length > 0"
              >
                <p class="profile-view__stat-label">Избранные теги:</p>
                <div class="d-flex gap-2 fs-6 mt-1">
                  <Tag v-for="tag in profile.tags" :key="tag.id" :tag="tag" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="profile-view__content col-md-9 pt-3">
          <Tabs
            :cache-lifetime="0"
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
              <LoadingCircle class="mx-auto my-auto" v-else />
            </Tab>
            <Tab :name="`Подписчики(${profile.followers_count})`">
              <div
                class="profile-view__following tab-pane"
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
                  class="profile-view__followers-list d-flex flex-wrap gap-3"
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
              <LoadingCircle class="mx-auto my-auto" v-else />
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
                  class="profile-view__following-list d-flex flex-wrap gap-3"
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
              <LoadingCircle class="mx-auto my-auto" v-else />
            </Tab>
          </Tabs>
        </div>
      </div>
    </div>
  </div>
  <LoadingCircle v-else class="mx-auto my-auto" />
</template>

<script setup lang="ts">
import LoadingCircle from "@/components/LoadingCircle.vue";
import Post from "@/components/Post.vue";
import ProfileListItemLarge from "@/components/ProfileListItemLarge.vue";
import Tag from "@/components/Tag.vue";
import { ChatListItemModel } from "@/models/ChatModel";
import type { ProfileDetailModel } from "@/models/ProfileModel";
import router from "@/router";
import ProfileDataService from "@/services/ProfileDataService";
import { computed, defineProps, onMounted, ref, watch } from "vue";
import { Tab, Tabs } from "vue3-tabs-component";
import { useStore } from "vuex";

const store = useStore();

const loading = ref(true);
const loadingPosts = ref(true);
const loadingFollowers = ref(true);
const loadingFollowing = ref(true);
const loadingToggleFollow = ref(false);
const loadingProfile = computed(() => store.getters["profile/getLoading"]);
const loadingSendMesssage = ref(false);

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
const isAuth = computed(() => store.getters["profile/getProfile"].id > -1);
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
      if (profile.value.followers.length != profile.value.followers_count) {
        profile.value.followers_count = profile.value.followers.length;
      }
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
      if (profile.value.following.length != profile.value.following_count) {
        profile.value.following_count = profile.value.following.length;
      }
      loadingFollowing.value = false;
    }
  );
};

const sendMessage = async () => {
  if (!guestMode.value) return;

  console.log(profile.value);
  if (profile.value.chat_uuid) {
    router.push({
      name: "chat",
      params: { uuid: profile.value.chat_uuid },
    });
  } else {
    loadingSendMesssage.value = true;

    await ProfileDataService.createChatWithProfile(profile.value.username)
      .then((response: ChatListItemModel) => {
        router.push({
          name: "chat",
          params: { uuid: response.uuid },
        });
      })
      .finally(() => {
        loadingSendMesssage.value = false;
      });
  }
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
  if (isAuth.value) {
    await ProfileDataService.followProfile(props.username);
  } else {
    router.push({ name: "login" });
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
  border-top-left-radius: 0.4rem !important;
  border-top-right-radius: 0.4rem !important;
}

.nav-item:hover {
  color: var(--light) !important;
}

.nav-item-active {
  text-decoration: underline;
  text-decoration-color: var(--primary);
}

.nav-item-link {
  display: flex;
  justify-content: center;
  color: var(--light);
}

.nav-item-link:hover {
  color: var(--light) !important;
}

.tab-panels-wrapper {
  display: flex;
  gap: 1rem;
}
</style>

<style scoped>
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
  margin: 0;
}

.profile-view__stat-label {
  color: var(--primary);
  font-weight: bold;
  /* text-decoration: underline;
  text-decoration-color: var(--primary); */
}
</style>
