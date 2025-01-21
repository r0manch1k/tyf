import auth from "@/stores/modules/auth";
import category from "@/stores/modules/category";
import collection from "@/stores/modules/collection";
import error from "@/stores/modules/error";
import pagination from "@/stores/modules/pagination";
import profile from "@/stores/modules/profile";
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
    pagination,
  },
});
