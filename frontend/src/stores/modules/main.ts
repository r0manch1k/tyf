import { ActionTree, GetterTree, MutationTree } from "vuex"

class State {
  showErrorPage = false;
  authMessage = { text: "", type: ""};
}

const getters: GetterTree<State, unknown> = {
  getShowErrorPage: (state) => state.showErrorPage, 
};

const mutations: MutationTree<State> = {
  setShowErrorPage: (state, payload: boolean) => {
    state.showErrorPage = payload;
  },
  setAuthMessage(state, message) {
    state.authMessage.text = message.text;
    state.authMessage.type = message.type;
  }
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
