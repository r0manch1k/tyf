import { ActionTree, GetterTree, MutationTree } from "vuex";
import type SearchModel from "@/models/SearchModel";

class State {
  pageId = 0;
  fetching = false;
  searchInput: SearchModel = {
    query: "",
    method: "full",
  };
}

const getters: GetterTree<State, unknown> = {
  getCurrentPostsPage: (state) => state.pageId,
  getFetchingStatus: (state) => state.fetching,
  getSearchInput: (state) => state.searchInput,
};

const mutations: MutationTree<State> = {
  setSearchInput(state, payload) {
    state.searchInput.query = payload.query;
    state.searchInput.method = payload.method;
  },
  incrementPostsPage: (state) => {
    state.pageId = state.pageId + 1;
  },
  enablePostsFetching: (state) => {
    state.pageId = 0;
    state.fetching = true;
  },
  disablePostsFetching: (state) => {
    state.pageId = 0;
    state.fetching = false;
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
