import { createStore } from "vuex";
import profile from "@/stores/modules/profile";
import main from "@/stores/modules/main";

export default createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    profile,
    main,
  },
});
