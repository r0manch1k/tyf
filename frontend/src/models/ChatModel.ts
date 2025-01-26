import type { ProfileListItemModel } from "@/models/ProfileModel";
import type MessageChatModel from "@/models/MessageChatModel";

export default interface ChatModel {
  id: number;
  uuid: string;
  name: string;
  participants: ProfileListItemModel[];
  messages: MessageChatModel[];
  last_message: MessageChatModel;
  created_at: string;
  updated_at: string;
  thumbnail: string;
}

export type ChatListItemModel = Omit<ChatModel, "messages">;

export type ChatDetailModel = Omit<ChatModel, "last_message" | "thumbnail">;
