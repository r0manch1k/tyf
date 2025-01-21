import { GetterTree, MutationTree } from "vuex";

class State {
  pageId = 0;
  fetching = false;
}

const getters: GetterTree<State, unknown> = {
  getCurrentPostsPage: (state) => state.pageId,
  getFetchingStatus: (state) => state.fetching,
};

const mutations: MutationTree<State> = {
  incrementPostsPage: (state) => {
    state.pageId = state.pageId + 1;
  },
  enablePostsFetching: (state) => {
    state.pageId = 0;
    state.fetching = true;
  },
  disablePostsFetching: (state) => {
    state.pageId = 0;
    state.fetching = false;
  },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
};
