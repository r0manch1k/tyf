import api from "@/stores/services/api";
import type PostModel from "@/models/PostModel";

class PostDataService {
  async getAllPosts(): Promise<PostModel[]> {
    let data: { data: PostModel[] } = { data: [] as PostModel[] };
    await api
      .get("/posts/")
      .then((response: { data: PostModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
}

export default new PostDataService();
