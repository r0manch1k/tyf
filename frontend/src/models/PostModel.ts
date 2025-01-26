import BookmarkPostModel from "@/models/BookmarkPostModel";
import CategoryModel from "@/models/CategoryModel";
import CollectionModel from "@/models/CollectionModel";
import CommentModel from "@/models/CommentModel";
import MediaModel from "@/models/MediaModel";
import ProfileModel from "@/models/ProfileModel";
import TagModel from "@/models/TagModel";

export default interface PostModel {
  id: number;
  category: CategoryModel;
  collections: CollectionModel[];
  tags: TagModel[];
  media: MediaModel[];
  comments: CommentModel[];
  active: boolean;
  title: string;
  content: string;
  identifier: string;
  created_at: string;
  updated_at: string;
  author: ProfileModel;
  description: string;
  filetypes: string[];
  thumbnail?: string;
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
