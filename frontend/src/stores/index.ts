import auth from "@/stores/modules/auth";
import category from "@/stores/modules/category";
import chat from "@/stores/modules/chat";
import collection from "@/stores/modules/collection";
import error from "@/stores/modules/error";
import notification from "@/stores/modules/notification";
import pagination from "@/stores/modules/pagination";
import profile from "@/stores/modules/profile";
import registry from "@/stores/modules/registry";
import search from "@/stores/modules/search";
import { createStore } from "vuex";

export default createStore({
  state: {},
  getters: {},
  mutations: {},
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
    search,
  },
});
