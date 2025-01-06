import ProfileModel from "@/models/ProfileModel";

export default interface BookmarkPostModel {
  id: number;
  profile: ProfileModel;
  created_at: string;
}
