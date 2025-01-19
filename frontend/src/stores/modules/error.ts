import { ActionTree, GetterTree, MutationTree } from "vuex";

class State {
  showErrorPage = false;
}

const getters: GetterTree<State, unknown> = {
  getShowErrorPage: (state) => state.showErrorPage,
};

const mutations: MutationTree<State> = {
  setShowErrorPage: (state, payload: boolean) => {
    state.showErrorPage = payload;
  },
};

const actions: ActionTree<State, unknown> = {
  setShowErrorPage: ({ commit }, payload: boolean) => {
    commit("setShowErrorPage", payload);
  },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
