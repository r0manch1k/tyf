import type { ProfileListItemModel } from "@/models/ProfileModel";

export default interface MessageChatModel {
  id: number;
  text: string;
  author: ProfileListItemModel;
  created_at: string;
  updated_at: string;
}
