import MediaModel from "./MediaModel";
import PostModel from "./PostModel";
import ProfileModel from "./ProfileModel";

export default interface CommentModel {
  identifier: string;
  content: string;
  stars: number;
  created_at: string;
  update_at: string;
  active: boolean;
  media: MediaModel;
  post: PostModel;
  author: ProfileModel;
  parent: number;
  replies: CommentModel[];
}
