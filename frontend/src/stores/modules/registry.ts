import { GetterTree, MutationTree, ActionTree } from "vuex";
import type UniversityModel from "@/models/UniversityModel";
import type MajorModel from "@/models/MajorModel";
import RegistryDataService from "@/services/RegistryDataService";

class State {
  universities: UniversityModel[] = [];
  majors: MajorModel[] = [];
  loading = false;
}

const getters: GetterTree<State, unknown> = {
  getUniversities: (state) => state.universities,
  getMajors: (state) => state.majors,
  getLoading: (state) => state.loading,
};

const mutations: MutationTree<State> = {
  setUniversities: (state, universities: UniversityModel[]) =>
    (state.universities = universities),
  setMajors: (state, majors: MajorModel[]) => (state.majors = majors),
  setLoading: (state, loading: boolean) => (state.loading = loading),
};

const actions: ActionTree<State, unknown> = {
  fetchUniversities: async ({ commit }) => {
    commit("setLoading", true);
    await RegistryDataService.getAllUniversities()
      .then((response) => {
        commit("setUniversities", response);
      })
      .catch((error) => {
        console.error(error);
      });
    commit("setLoading", false);
  },
  fetchMajors: async ({ commit }) => {
    commit("setLoading", true);
    await RegistryDataService.getAllMajors()
      .then((response) => {
        commit("setMajors", response);
      })
      .catch((error) => {
        console.error(error);
      });
    commit("setLoading", false);
  },
  setLoading: ({ commit }, loading: boolean) => {
    commit("setLoading", loading);
  },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
