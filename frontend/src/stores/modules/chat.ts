import { ActionTree, GetterTree, MutationTree } from "vuex";
import ChatModel from "@/models/ChatModel";
import ProfileDataService from "@/services/ProfileDataService";
import ChatDataService from "@/services/ChatDataService";
import { set } from "lodash";

class State {
  storedChats: Record<string, ChatModel> = {};
}

const getters: GetterTree<State, unknown> = {
  getChats: (state) => {
    return state.storedChats;
  },
  getChatByUUID: (state) => (uuid: string) => {
    return state.storedChats[uuid];
  },
};

const mutations: MutationTree<State> = {
  setStoredChats: (state, payload) => {
    state.storedChats = payload;
  },
  setChat: (state, payload) => {
    set(state.storedChats, payload.uuid, payload);
  },
  setMessages: (state, payload) => {
    set(state.storedChats, payload.uuid, {
      ...state.storedChats[payload.uuid],
      messages: payload.messages,
    });
  },
};

const actions: ActionTree<State, unknown> = {
  fetchProfileChats: async ({ commit }, username: string) => {
    const data = await ProfileDataService.getProfileChats(username);
    commit("setStoredChats", data);
  },
  fetchChatByUUID: async ({ commit, state }, uuid: string) => {
    if (uuid in state.storedChats) {
      return;
    }
    const data = await ChatDataService.getChatByUUID(uuid);
    commit("setChat", data);
  },
  addMessages: async ({ commit }, payload) => {
    commit("setMessages", payload);
  },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
