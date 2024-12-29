import { createStore } from "vuex";
import profile from "@/stores/modules/profile";
import main from "@/stores/modules/main";
import collection from "@/stores/modules/collection";
import category from "@/stores/modules/category";

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
