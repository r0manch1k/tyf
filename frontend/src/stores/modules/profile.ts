import { GetterTree, MutationTree, ActionTree, createStore } from "vuex";
import type ProfileModel from "@/models/ProfileModel";
import type UniversityModel from '@/models/UniversityModel';
import type MajorModel from "@/models/MajorModel";
import ProfileDataService from "@/services/ProfileDataService";

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
    tags: null,
    is_following: false,
    is_followed: false,
    following_count: 0,
    followers_count: 0,
  };
  loading = false;
}

const getters: GetterTree<State, unknown> = {
  getProfile: (state) => state.profile,
  getLoading: (state) => state.loading,
};

const mutations: MutationTree<State> = {
  setProfile: (state, profile: ProfileModel) => (state.profile = profile),
  setLoading: (state, loading: boolean) => (state.loading = loading),
};

const actions: ActionTree<State, unknown> = {
  fetchProfile: async ({ commit }) => {
    commit("setLoading", true);
    await ProfileDataService.getMyProfile().then((response) => {
      commit("setProfile", response);
      commit("setLoading", false);
      return response;
    });
  },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
