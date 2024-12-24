import { GetterTree, MutationTree, ActionTree } from "vuex";
import type ProfileModel from "@/models/ProfileModel";
import ProfileDataService from "@/stores/services/ProfileDataService";

class State {
  cachedProfiles: { [key: string]: ProfileModel } = {};
}

const getters: GetterTree<State, unknown> = {
  getProfileByUsername: (state) => (username: string) => {
    return state.cachedProfiles[username];
  },
  getRecentProfiles: (state) => (value: number) => {
    const profilesArray = Object.values(state.cachedProfiles);
    profilesArray.sort(
      (a, b) =>
        new Date(b.date_joined).getTime() - new Date(a.date_joined).getTime()
    );
    return profilesArray.slice(0, value);
  },
};

const mutations: MutationTree<State> = {
  setCachedProfiles: (state, payload) => {
    state.cachedProfiles = payload;
  },
};

const actions: ActionTree<State, unknown> = {
  fetchProfileByUsername: async ({ commit, state }, username: string) => {
    const data = await ProfileDataService.getProfileByUsername(username);
    commit("setCachedProfiles", {
      ...state.cachedProfiles,
      [username]: data,
    });
  },
  fetchRecentProfiles: async ({ commit }) => {
    const data = await ProfileDataService.getRecentProfiles();
    commit("setCachedProfiles", data);
  },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
