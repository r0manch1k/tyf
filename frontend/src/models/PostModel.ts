import CategoryModel from "@/models/CategoryModel";
import CollectionModel from "@/models/CollectionModel";
import TagModel from "@/models/TagModel";
import ProfileModel from "@/models/ProfileModel";
import CommentModel from "@/models/CommentModel";
import MediaModel from "@/models/MediaModel";


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
  stars: number;
  created_at: string;
  updated_at: string;
  author: ProfileModel;
  bookmarks: number;
  description: string;
  filetypes: string[];
  thumbnail: string;
}
