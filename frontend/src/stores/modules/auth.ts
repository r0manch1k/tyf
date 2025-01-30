import type MessageModel from "@/models/MessageModel";
import { ActionTree, GetterTree, MutationTree } from "vuex";

class State {
  login = false;
  loading = false;
  showMessage = false;
  refreshAttempts = 0;
  message: MessageModel = {
    text: "",
    type: "",
  };
}

const getters: GetterTree<State, unknown> = {
  getLogin: (state) => state.login,
  getLoading: (state) => state.loading,
  getMessage: (state) => state.message,
  getShowMessage: (state) => state.showMessage,
  getRefreshAttempts: (state) => state.refreshAttempts,
};

const mutations: MutationTree<State> = {
  incrementRefreshAttempts: (state) => {
    state.refreshAttempts = state.refreshAttempts + 1;
  },
  clearRefreshAttempts: (state) => {
    state.refreshAttempts = 0;
  },
  setLogin: (state, payload: boolean) => {
    state.login = payload;
  },
  setLoading: (state, payload: boolean) => {
    state.loading = payload;
  },
  setShowMessage: (state, payload: boolean) => {
    state.showMessage = payload;
  },
  setMessage(state, message) {
    state.message.text = message.text;
    state.message.type = message.type;
  },
};

const actions: ActionTree<State, unknown> = {
  setLogin: ({ commit }, payload: boolean) => {
    commit("setLogin", payload);
  },
  setMessage({ commit }, message) {
    commit("setMessage", message);
  },
  incrementRefreshAttempts: ({ commit }) => {
    commit("incrementRefreshAttempts");
  },
  clearRefreshAttempts: ({ commit }) => {
    commit("clearRefreshAttempts");
  },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
