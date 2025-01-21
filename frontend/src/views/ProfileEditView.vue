<template>
  <div class="profile-edit container" v-if="!loading">
    <div class="profile-edit__header row">
      <h1 class="col-12 text-center">Edit Profile</h1>
    </div>
    <div class="profile-edit__content row">
      <div class="profile-edit__content__left col-md-4">
        <div class="profile-edit__content__left__avatar text-center mb-4">
          <img
            src="https://via.placeholder.com/150"
            alt="Avatar"
            class="img-fluid rounded-circle"
          />
        </div>
        <div class="profile-edit__content__left__username mb-3">
          <h2>Username</h2>
          <p>username</p>
        </div>
        <div class="profile-edit__content__left__email mb-3">
          <h2>Email</h2>
          <p>email</p>
        </div>
        <div class="profile-edit__content__left__bio mb-3">
          <h2>Bio</h2>
          <p>bio</p>
        </div>
      </div>
      <div class="profile-edit__content__right col-md-8">
        <div class="profile-edit__content__right__form">
          <form>
            <div class="form-group mb-3">
              <label for="username">Username</label>
              <input
                type="text"
                id="username"
                name="username"
                class="form-control"
              />
            </div>
            <div class="form-group mb-3">
              <label for="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                class="form-control"
              />
            </div>
            <div class="form-group mb-3">
              <label for="bio">Bio</label>
              <textarea id="bio" name="bio" class="form-control"></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Save</button>
          </form>
        </div>
      </div>
    </div>
  </div>
  <LoadingCircle v-else />
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";
import ProfileDataService from "@/services/ProfileDataService";
import type { ProfileDetailModel } from "@/models/ProfileModel";
import LoadingCircle from "@/components/LoadingCircle.vue";

const store = useStore();
const loading = ref(true);
const profile = computed<ProfileDetailModel>(
  () => store.getters["profile/getProfile"]
);

onMounted(async () => {
  await store.dispatch("profile/fetchProfile");
  await ProfileDataService.getProfileByUsername(profile.value.username);
});
</script>
