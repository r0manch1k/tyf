import type PostListItemModel from "@/models/PostModel";
import type UniversityModel from "@/models/UniversityModel";
import type MajorModel from "@/models/MajorModel";

export default interface ProfileModel {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  middle_name: string;
  university: UniversityModel;
  major: MajorModel;
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
}

export type ProfileListItemModel = Pick<
  ProfileModel,
  "username" | "avatar" | "date_joined" | "posts_count" | "points"
>;

export type ProfileDetailModel = Omit<ProfileModel, "posts_count">;
