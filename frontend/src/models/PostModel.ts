import CategoryModel from "@/models/CategoryModel";
import CollectionModel from "@/models/CollectionModel";
import TagModel from "@/models/TagModel";
import ProfileModel from "@/models/ProfileModel";
import BookmarkPostModel from "@/models/BookmarkPostModel";

export default interface PostModel {
  id: number;
  category: CategoryModel;
  collections: CollectionModel[];
  tags: TagModel[];
  title: string;
  content: string;
  identifier: string;
  created_at: string;
  updated_at: string;
  author: ProfileModel;
  description: string;
  filetypes: string[];
  thumbnail: string;
  comments: number;
  media: string[];
  bookmarks: BookmarkPostModel[];
  comments_count: number;
  bookmarks_count: number;
}

export type PostListItemModel = Omit<
  PostModel,
  "content" | "comments" | "bookmarks" | "media"
>;

export type PostDetailModel = Omit<
  PostModel,
  "comments_count" | "bookmarks_count"
>;
