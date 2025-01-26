import auth from "@/stores/modules/auth";
import category from "@/stores/modules/category";
import collection from "@/stores/modules/collection";
import error from "@/stores/modules/error";
import pagination from "@/stores/modules/pagination";
import profile from "@/stores/modules/profile";
import registry from "@/stores/modules/registry";
import chat from "@/stores/modules/chat";
import notification from "@/stores/modules/notification";
import { createStore } from "vuex";

export default createStore({
  state: {
    isSuggestionsOpen: false,
  },
  getters: {
    isSuggestionsOpen: (state) => state.isSuggestionsOpen,
  },
  mutations: {
    setSuggestionsOpen(state, isOpen) {
      state.isSuggestionsOpen = isOpen;
    },
  },
  actions: {},
  modules: {
    profile,
    error,
    collection,
    category,
    auth,
    registry,
    pagination,
    chat,
    notification,
  },
});
