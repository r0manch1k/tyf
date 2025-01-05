import api from "@/stores/services/api";
import type PostModel from "@/models/PostModel";
import type CategoryModel from "@/models/CategoryModel";
import type CollectionModel from "@/models/CollectionModel";
import type TagModel from "@/models/TagModel";
import type ProfileModel from "@/models/ProfileModel";

class PostDataService {
  async getAllPosts(): Promise<PostModel[]> {
    let data: { data: PostModel[] } = { data: [] as PostModel[] };
    await api
      .get("/posts/")
      .then((response: { data: PostModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
  async createPost(post: PostModel): Promise<PostModel> {
    let data: { data: PostModel } = { data: {} as PostModel };
    await api
      .post("/posts/", post)
      .then((response: { data: PostModel }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
  getNewPost(): PostModel {
    return {
      id: 0,
      category: {} as CategoryModel,
      collections: [] as CollectionModel[],
      tags: [] as TagModel[],
      media: [] as string[],
      comments: 0,
      active: false,
      title: "",
      content: "",
      identifier: "",
      stars: 0,
      created_at: "",
      updated_at: "",
      author: {} as ProfileModel,
      bookmarks: 0,
      description: "",
      filetypes: [] as string[],
      thumbnail: "",
    };
  }
}

export default new PostDataService();
