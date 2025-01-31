import { ActionTree, GetterTree, MutationTree } from "vuex";
import type NotificationModel from "@/models/NotificationModel";
import NotificationDataService from "@/services/NotificationDataService";

class State {
  notifications: NotificationModel[] = [];
}

const getters: GetterTree<State, unknown> = {
  getNotifications: (state) => state.notifications,
};

const mutations: MutationTree<State> = {
  setNotifications: (state, payload) => {
    state.notifications = payload;
  },
  addNotification: (state, notification: NotificationModel) => {
    state.notifications = [notification, ...state.notifications];
  },
  setNotificationRead: (state, id: number) => {
    const notification = state.notifications.find((n) => n.id === id);
    if (notification) {
      notification.read = true;
    }
  },
  setAllNotificationsRead: (state) => {
    state.notifications.forEach((n) => (n.read = true));
  },
};

const actions: ActionTree<State, unknown> = {
  fetchUnreadNotifications: async ({ commit }) => {
    const data = await NotificationDataService.getUnreadNotifications();
    commit("setNotifications", data);
  },
  fetchAllNotifications: async ({ commit }) => {
    const data = await NotificationDataService.getAllNotifications();
    commit("setNotifications", data);
  },
  deleteReadNotifications: async ({ commit }) => {
    await NotificationDataService.deleteReadNotifications();
    const data = await NotificationDataService.getAllNotifications();
    commit("setNotifications", data);
  },
  readNotification: async ({ commit }, id: number) => {
    await NotificationDataService.readNotification(id);
    commit("setNotificationRead", id);
  },
  addNotification: ({ commit }, notification: NotificationModel) => {
    commit("addNotification", notification);
  },
  readAllNotifications: async ({ commit }) => {
    await NotificationDataService.readAllNotifications();
    commit("setAllNotificationsRead");
  },
};

export default {
  namespaced: true,
  state: new State(),
  getters,
  mutations,
  actions,
};
