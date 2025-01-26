import { GetterTree, MutationTree, ActionTree } from "vuex";
import type ProfileModel from "@/models/ProfileModel";
import type UniversityModel from "@/models/UniversityModel";
import ProfileDataService from "@/services/ProfileDataService";
import type MajorModel from "@/models/MajorModel";

class State {
  profile: ProfileModel | null = {
    id: -1,
    email: "",
    username: "",
    first_name: "",
    last_name: "",
    middle_name: "",
    university: null as UniversityModel | null,
    major: null as MajorModel | null,
    date_of_birth: "",
    date_joined: "",
    bio: "",
    avatar: "",
    points: 0,
    awards: 0,
    telegram: "",
    vkontakte: "",
    telegram_alias: "",
    vkontakte_alias: "",
    posts_count: 0,
    followers: [],
    following: [],
    posts: [],
    tags: [],
    is_following_request_user: false,
    is_followed_by_request_user: false,
    following_count: 0,
    followers_count: 0,
  };
  loading = false;
}

const getters: GetterTree<State, unknown> = {
  getProfile: (state) => state.profile,
  getLoading: (state) => state.loading,
  getDefaultProfile: () => new State().profile,
  getIsAuth: (state) =>
    (state.profile && state.profile.id > 0) ||
    localStorage.getItem("accessToken") !== "",
};

const mutations: MutationTree<State> = {
  setProfile: (state, profile: ProfileModel) => (state.profile = profile),
  setLoading: (state, loading: boolean) => (state.loading = loading),
};

const actions: ActionTree<State, unknown> = {
  fetchProfile: async ({ commit }) => {
    commit("setLoading", true);
    await ProfileDataService.getMyProfile()
      .then((response) => {
        commit("setProfile", response);
      })
      .catch((error) => {
        if (error.status === 401) {
          commit("setProfile", new State().profile);
        }
      })
      .finally(() => {
        commit("setLoading", false);
      });
  },
  setDefault: ({ commit }) => {
    commit("setProfile", new State().profile);
    commit("setLoading", new State().loading);
  },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
