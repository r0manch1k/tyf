import api from "@/stores/services/api";
import type PostListItemModel from "@/models/PostModel";
import type PostDetailModel from "@/models/PostModel";
// import type CategoryModel from "@/models/CategoryModel";
// import type CollectionModel from "@/models/CollectionModel";
// import type TagModel from "@/models/TagModel";
// import type ProfileModel from "@/models/ProfileModel";
// import PostDetailView from "@/views/PostDetailView.vue";

class PostDataService {
  async getAllPosts(): Promise<PostListItemModel[]> {
    let data: { data: PostListItemModel[] } = {
      data: [] as PostListItemModel[],
    };
    await api
      .get("/posts/")
      .then((response: { data: PostListItemModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
  async getPostByIdentifier(identifier: string): Promise<PostDetailModel> {
    let data: { data: PostDetailModel } = { data: {} as PostDetailModel };
    await api
      .get(`/posts/${identifier}`)
      .then((response: { data: PostDetailModel }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
}

export default new PostDataService();
