import type NotificationModel from "@/models/NotificationModel";
import api from "@/stores/services/api";

class NotificationDataService {
  async getNotifications(): Promise<NotificationModel[]> {
    let data: { data: NotificationModel[] } = {
      data: [] as NotificationModel[],
    };
    await api
      .get("/notifications/")
      .then((response: { data: NotificationModel[] }) => {
        data = response;
      })
      .catch((error: unknown) => {
        return Promise.reject(error);
      });
    return data.data;
  }
  async getUnreadNotifications(): Promise<NotificationModel[]> {
    let data: { data: NotificationModel[] } = {
      data: [] as NotificationModel[],
    };
    await api
      .get("/notifications/unread/")
      .then((response: { data: NotificationModel[] }) => {
        data = response;
      })
      .catch((error: unknown) => {
        return Promise.reject(error);
      });

    return data.data;
  }
  async readNotification(id: number): Promise<void> {
    await api
      .put(`/notifications/${id}/read/`)
      .then((response) => {
        return Promise.resolve(response);
      })
      .catch((error: unknown) => {
        return Promise.reject(error);
      });
  }
  async readAllNotifications(): Promise<void> {
    await api
      .put("/notifications/read-all/")
      .then((response) => {
        return Promise.resolve(response);
      })
      .catch((error: unknown) => {
        return Promise.reject(error);
      });
  }
}

export default new NotificationDataService();
