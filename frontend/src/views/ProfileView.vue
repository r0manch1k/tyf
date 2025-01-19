<template>
  <div v-if="!loading && !loadingProfile" class="profile-view px-5">
    <div class="profile-view__container container-fluid p-0">
      <div class="profile-view__row row">
        <div class="profile-view__sidebar col-3">
          <div
            class="profile-view__meta d-flex flex-column gap-3 p-3 align-items-center"
          >
            <img
              :src="profile.avatar"
              alt="avatar"
              class="profile-view__avatar img-fluid rounded-circle"
              style="width: max-content; height: max-content"
            />
            <div class="profile-view__stats d-flex flex-column gap-1">
              <div
                class="profile-view__username text-primary w-100 text-start fs-3"
              >
                {{ profile.username }}
              </div>
              <div
                class="profile-view__bio fs-6 text-secondary-xx-light w-100 text-start"
              >
                {{ profile.bio }}
              </div>
            </div>

            <!-- <div class="profile-view__tags fs-6 text-light w-100 text-start">
              <div class="profile-view__tags-list d-flex flex-wrap gap-2">
                <Tag v-for="tag in profile.tags" :key="tag.id" :tag="tag" />
              </div>
            </div> -->
            <!-- <div
              v-if="profile.telegram || profile.vkontakte"
              class="profile-view__social-links fs-6 text-light text-center d-flex w-100 gap-3"
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
            </div> -->

            <div class="profile-view__actions d-flex flex-column w-100 gap-2">
              <button
                v-if="isAuth && guestMode"
                @click="toggleFollow"
                class="btn btn-action text-decoration-none text-light"
                :class="{
                  'action-checked': profile.is_following,
                  'action-unchecked': !profile.is_following,
                }"
                :disabled="loadingToggleFollow"
              >
                <span v-if="!loadingToggleFollow">
                  {{ profile.is_following ? "Отписаться" : "Подписаться" }}
                </span>
                <LoadingCircle v-else />
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
          </div>
        </div>

        <div class="profile-view__content col-9">
          <Tabs
            nav-item-class="profile-view__tab-item nav-item"
            nav-item-active-class="profile-view__tab-item--active nav-item-active"
            nav-item-link-class="profile-view__tab-link nav-item-link"
            nav-class="profile-view__tab-panels-wrapper tab-panels-wrapper"
            @changed="onTabChanged"
          >
            <Tab :name="`Публикации (${profile.posts_count})`">
              <div class="profile-view__posts tab-pane" v-if="!loadingPosts">
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
              <LoadingCircle v-else />
            </Tab>
            <Tab :name="`Подписчики (${profile.followers_count})`">
              <div
                class="profile-view__followers tab-pane"
                v-if="!loadingFollowers"
              >
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
              <LoadingCircle v-else />
            </Tab>
            <Tab :name="`Подписки (${profile.following_count})`">
              <div
                class="profile-view__following tab-pane"
                v-if="!loadingFollowing"
              >
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
  <h1>{{ store.state.profile.username + props.username }}</h1>
</template>

<script setup lang="ts">
import LoadingCircle from "@/components/LoadingCircle.vue";
import Post from "@/components/Post.vue";
import { computed, defineProps, onMounted, ref } from "vue";
import { Tab, Tabs } from "vue3-tabs-component";
import { useStore } from "vuex";
// import Tag from "@/components/Tag.vue";
import type ProfileDetailModel from "@/models/ProfileModel";
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

const profile = ref<ProfileDetailModel>(store.getters["profile/getProfile"]);
const isAuth = computed(() => profile.value.id > -1);
const loadingProfile = computed(() => store.state.profile.loading);
const guestMode = computed(
  () => store.state.profile.username != props.username
);

onMounted(async () => {
  await fetchProfile();
});

const fetchProfile = async () => {
  loading.value = true;
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
  if (isAuth.value && guestMode && profile.value.is_following) {
    await ProfileDataService.unfollowProfile(props.username);
  } else {
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
  width: 100%;
  display: block;
  background-color: var(--dark-light);
  color: var(--light);
  border-top-left-radius: 0.4rem !important;
  border-top-right-radius: 0.4rem !important;
  padding: 0.5rem 1rem;
  font-weight: 700;
}

.nav-item:hover {
  color: var(--light) !important;
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

#posts-nav button.active {
  border-bottom: 1px solid var(--secondary-x-light);
}
</style>
