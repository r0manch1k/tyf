import { ActionTree, GetterTree, MutationTree } from "vuex";
import ChatModel from "@/models/ChatModel";
import ProfileDataService from "@/services/ProfileDataService";
import ChatDataService from "@/services/ChatDataService";
import { set, merge } from "lodash";
import type MessageChatModel from "@/models/MessageChatModel";

class State {
  chats: Record<string, ChatModel> = {};
  default: ChatModel = {
    id: 0,
    uuid: "",
    name: "",
    participants: [],
    messages: [],
    last_message: {
      id: -1,
      text: "",
      author: {
        id: -1,
        username: "",
        avatar: "",
        date_joined: "",
        posts_count: 0,
        points: 0,
      },
      created_at: "",
      updated_at: "",
    },
    created_at: "",
    updated_at: "",
    thumbnail: "",
  };
  editMode = false;
}

const getters: GetterTree<State, unknown> = {
  getChats: (state) => {
    return state.chats;
  },
  getChatByUUID: (state) => (uuid: string) => {
    return state.chats[uuid] || state.default;
  },
  getDefaultChat: (state) => {
    return state.default;
  },
  getDefaultMessage: (state) => {
    return state.default.last_message;
  },
  getEditMode: (state) => {
    return state.editMode;
  },
};

const mutations: MutationTree<State> = {
  setChats: (state, payload: ChatModel[]) => {
    for (const chat of payload) {
      if (state.chats[chat.uuid]) {
        merge(state.chats[chat.uuid], chat);
      } else {
        set(state.chats, chat.uuid, chat);
      }
    }
  },
  setChat: (state, payload: { uuid: string; message: ChatModel }) => {
    if (state.chats[payload.uuid]) {
      merge(state.chats[payload.uuid], payload);
    } else {
      set(state.chats, payload.uuid, payload);
    }
  },
  setMessage: (state, payload: { uuid: string; message: MessageChatModel }) => {
    if (state.chats[payload.uuid]) {
      state.chats[payload.uuid].messages.push(payload.message);
    }
  },
  setLastMessage: (
    state,
    payload: { uuid: string; message: MessageChatModel }
  ) => {
    if (state.chats[payload.uuid]) {
      state.chats[payload.uuid].last_message = payload.message;
    }
  },
  setEditMode: (state, payload: boolean) => {
    state.editMode = payload;
  },
};

const actions: ActionTree<State, unknown> = {
  fetchProfileChats: async ({ commit }, username: string) => {
    const data = await ProfileDataService.getProfileChats(username);
    commit("setChats", data);
  },
  fetchChatByUUID: async ({ commit }, uuid: string) => {
    const data = await ChatDataService.getChatByUUID(uuid).catch((error) => {
      return Promise.reject(error);
    });
    commit("setChat", data);
  },
  addMessage: (
    { commit },
    payload: { uuid: string; message: MessageChatModel }
  ) => {
    commit("setMessage", payload);
    commit("setLastMessage", payload);
  },
  setEditMode: ({ commit }, payload: boolean) => {
    commit("setEditMode", payload);
  },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
