import TagModel from "@/models/TagModel";
import api from "@/stores/services/api";

class TagDataService {
  async getAllTags(): Promise<TagModel[]> {
    let data: { data: TagModel[] } = { data: [] as TagModel[] };
    await api
      .get("/tags/")
      .then((response: { data: TagModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
}

export default new TagDataService();
