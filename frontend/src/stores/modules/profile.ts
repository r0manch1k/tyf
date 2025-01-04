import { GetterTree, MutationTree, ActionTree } from "vuex";
import type ProfileModel from "@/models/ProfileModel";
import ProfileDataService from "@/services/ProfileDataService";

class State {
  storedProfiles: { [key: string]: ProfileModel } = {};
}

const getters: GetterTree<State, unknown> = {
  getProfileByUsername: (state) => (username: string) => {
    return state.storedProfiles[username];
  },
  getRecentProfiles: (state) => (value: number) => {
    const profilesArray = Object.values(state.storedProfiles);
    profilesArray.sort(
      (a, b) =>
        new Date(b.date_joined).getTime() - new Date(a.date_joined).getTime()
    );
    return profilesArray.slice(0, value);
  },
};

const mutations: MutationTree<State> = {
  setStoredProfiles: (state, payload) => {
    state.storedProfiles = payload;
  },
};

const actions: ActionTree<State, unknown> = {
  fetchProfileByUsername: async ({ commit, state }, username: string) => {
    const data = await ProfileDataService.getProfileByUsername(username);
    commit("setStoredProfiles", {
      ...state.storedProfiles,
      [username]: data,
    });
  },
  fetchRecentProfiles: async ({ commit }) => {
    const data = await ProfileDataService.getRecentProfiles();
    commit("setStoredProfiles", data);
  },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
