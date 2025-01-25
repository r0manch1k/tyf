import { ActionTree, GetterTree, MutationTree } from "vuex";
import type CategoryModel from "@/models/CategoryModel";
import CategoryDataService from "@/services/CategoryDataService";

class State {
  storedCategories: CategoryModel[] = [];
}

const getters: GetterTree<State, unknown> = {
  getCategories: (state) => {
    return state.storedCategories;
  },
};

const mutations: MutationTree<State> = {
  setStoredCategories: (state, payload) => {
    state.storedCategories = payload;
  },
};

const actions: ActionTree<State, unknown> = {
  fetchCategories: async ({ commit }) => {
    const data = await CategoryDataService.getAllCategories();
    commit("setStoredCategories", data);
  },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
