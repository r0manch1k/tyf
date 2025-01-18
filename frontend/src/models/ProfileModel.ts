import type PostListItemModel from "@/models/PostModel";
import type UniversityModel from "@/models/UniversityModel";
import type MajorModel from "@/models/MajorModel";
import type TagModel from "@/models/TagModel";

export default interface ProfileModel {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  middle_name: string;
  university: UniversityModel | null;
  major: MajorModel | null;
  date_of_birth: string;
  date_joined: string;
  bio: string;
  avatar: string;
  points: number;
  awards: number;
  telegram: string;
  vkontakte: string;
  telegram_alias: string;
  vkontakte_alias: string;
  posts_count: number;
  followers: ProfileListItemModel[];
  following: ProfileListItemModel[];
  posts: PostListItemModel[];
  tags: TagModel[] | null;
}

export type ProfileListItemModel = Pick<
  ProfileModel,
  "id" | "username" | "avatar" | "date_joined" | "posts_count" | "points"
>;

export type ProfileDetailModel = Omit<ProfileModel, "posts_count">;
