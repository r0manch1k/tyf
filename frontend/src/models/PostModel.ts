import CategoryModel from "@/models/CategoryModel";
import CollectionModel from "@/models/CollectionModel";
import TagModel from "@/models/TagModel";
import ProfileModel from "@/models/ProfileModel";

export default interface PostModel {
  id: number;
  category: CategoryModel;
  collections: CollectionModel[];
  tags: TagModel[];
  media: number;
  comments: number;
  active: boolean;
  title: string;
  content: string;
  identifier: string;
  stars: number;
  created_at: string;
  updated_at: string;
  author: ProfileModel;
  bookmarks: number;
}
