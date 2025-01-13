import { GetterTree, MutationTree, ActionTree } from "vuex";
import type ProfileModel from "@/models/ProfileModel";
import ProfileDataService from "@/services/ProfileDataService";
import type UniversityModel from "@/models/UniversityModel";
import type MajorModel from "@/models/MajorModel";

class State {
  profile: ProfileModel | null = {
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
  };
}

const getters: GetterTree<State, unknown> = {
  getProfile: (state) => state.profile,
};

const mutations: MutationTree<State> = {
  setProfile: (state, profile: ProfileModel) => (state.profile = profile),
};

const actions: ActionTree<State, unknown> = {
  // async fetchProfile({ commit }) {
  //   const profile = await ProfileDataService.getProfile();
  //   commit("setProfile", profile);
  // },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
