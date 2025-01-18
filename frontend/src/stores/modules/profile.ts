import { GetterTree, MutationTree, ActionTree } from "vuex";
import type ProfileModel from "@/models/ProfileModel";
import ProfileDataService from "@/services/ProfileDataService";
import type UniversityModel from "@/models/UniversityModel";
import type MajorModel from "@/models/MajorModel";
// import ProfileDataService from "@/services/ProfileDataService";

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
  };
}

const getters: GetterTree<State, unknown> = {
  getProfile: (state) => state.profile,
};

const mutations: MutationTree<State> = {
  setProfile: (state, profile: ProfileModel) => (state.profile = profile),
};

const actions: ActionTree<State, unknown> = {
  fetchProfile: async ({ commit }) => {
    const profile = await ProfileDataService.getMyProfile().then((response) => {
      console.log("Profile fetched", response);
      commit("setProfile", response);
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
