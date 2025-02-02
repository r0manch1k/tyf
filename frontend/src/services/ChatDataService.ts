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
      .then((response: { data: ChatDetailModel }) => (data = response))
      .catch((error: unknown) => console.error(error));
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
}

export default new ChatDataService();
