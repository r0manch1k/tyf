import { ActionTree, GetterTree, MutationTree } from "vuex";
import type SearchModel from "@/models/SearchModel";

class State {
  isSuggestionsOpen = false;
  searchInput: SearchModel = {
    query: "",
    method: "full",
  };
}

const getters: GetterTree<State, unknown> = {
  getSearchInput: (state) => state.searchInput,
  isSuggestionsOpen: (state) => state.isSuggestionsOpen,
};

const mutations: MutationTree<State> = {
  setSearchInput(state, payload) {
    state.searchInput.query = payload.query;
    state.searchInput.method = payload.method;
  },
  setSuggestionsOpen(state, isOpen) {
    state.isSuggestionsOpen = isOpen;
  },
};

const actions: ActionTree<State, unknown> = {
  updateSearchInput({ commit }, payload) {
    commit("setSearchInput", payload);
  }
}

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions
};
