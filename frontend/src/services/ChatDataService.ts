import type { ChatDetailModel, ChatListItemModel } from "@/models/ChatModel";
import type { MessageChatPayloadModel } from "@/models/MessageChatModel";
import type MessageChatModel from "@/models/MessageChatModel";
import api from "@/stores/services/api";

class ChatDataService {
  async getAllChats(): Promise<ChatListItemModel[]> {
    let data: { data: ChatListItemModel[] } = {
      data: [] as ChatListItemModel[],
    };
    await api
      .get("/chats/")
      .then((response: { data: ChatListItemModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
  async getChatByUUID(uuid: string): Promise<ChatDetailModel> {
    let data: { data: ChatDetailModel } = { data: {} as ChatDetailModel };
    await api
      .get(`/chats/${uuid}/`)
      .then((response) => {
        if (response.status === 200) {
          data = response;
        } else {
          return Promise.reject(response);
        }
      })
      .catch((error: unknown) => {
        return Promise.reject(error);
      });
    return data.data;
  }
  async sendMessage(
    uuid: string,
    message: MessageChatPayloadModel
  ): Promise<MessageChatModel> {
    let data: { data: MessageChatModel } = { data: {} as MessageChatModel };
    await api
      .post(`/chats/${uuid}/messages/`, message)
      .then((response: { data: MessageChatModel }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
  async updateChat(data: ChatDetailModel): Promise<void> {
    const uuid = data.uuid;
    await api
      .patch(`/chats/${uuid}/`, data)
      .then((response) => {
        if (response.status != 200) {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }
  async updateThumbnail(uuid: string, file: File): Promise<void> {
    const formData = new FormData();
    formData.append("thumbnail", file);
    await api
      .patch(`/chats/${uuid}/thumbnail/`, formData)
      .then((response) => {
        if (response.status != 200) {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }
}

export default new ChatDataService();
