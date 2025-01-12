import CollectionModel from "@/models/CollectionModel";
import api from "@/stores/services/api";

class CollectionDataService {
  async getAllCollections(): Promise<CollectionModel[]> {
    let data: { data: CollectionModel[] } = { data: [] as CollectionModel[] };
    await api
      .get("/collections/")
      .then((response: { data: CollectionModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
}

export default new CollectionDataService();
