import type NotificationModel from "@/models/NotificationModel";
import api from "@/stores/services/api";

class NotificationDataService {
  async getAllNotifications(): Promise<NotificationModel[]> {
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
  async deleteReadNotifications(): Promise<void> {
    // Should be a DELETE request or GET request?
    await api
      .get("/notifications/delete-read/")
      .then((response) => {
        return Promise.resolve(response);
      })
      .catch((error: unknown) => {
        return Promise.reject(error);
      });
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
