import { GetterTree, MutationTree, ActionTree } from "vuex";
import type CollectionModel from "@/models/CollectionModel";
import CollectionDataService from "@/stores/services/CollectionDataService";

class State {
  storedCollections: CollectionModel[] = [];
}

const getters: GetterTree<State, unknown> = {
  getCollections: (state) => {
    return state.storedCollections;
  },
};

const mutations: MutationTree<State> = {
  setStoredCollections: (state, payload) => {
    state.storedCollections = payload;
  },
};

const actions: ActionTree<State, unknown> = {
  fetchCollections: async ({ commit }) => {
    const data = await CollectionDataService.getAllCollections();
    commit("setStoredCollections", data);
  },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
