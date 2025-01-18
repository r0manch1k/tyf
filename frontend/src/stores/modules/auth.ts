import { ActionTree, GetterTree, MutationTree } from "vuex";
import type MessageModel from "@/models/MessageModel";

class State {
  login = false;
  loading = false;
  message: MessageModel = {
    text: "",
    type: "",
  };
}

const getters: GetterTree<State, unknown> = {
  getLogin: (state) => state.login,
  getLoading: (state) => state.loading,
  getMessage: (state) => state.message,
};

const mutations: MutationTree<State> = {
  setLogin: (state, payload: boolean) => {
    state.login = payload;
  },
  setLoading: (state, payload: boolean) => {
    state.loading = payload;
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
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
