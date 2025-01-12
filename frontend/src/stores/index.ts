import category from "@/stores/modules/category";
import collection from "@/stores/modules/collection";
import main from "@/stores/modules/main";
import profile from "@/stores/modules/profile";
import { createStore } from "vuex";

export default createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    profile,
    main,
    collection,
    category,
  },
});
