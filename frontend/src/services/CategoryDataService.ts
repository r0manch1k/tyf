import CategoryModel from "@/models/CategoryModel";
import api from "@/stores/services/api";

class CategoryDataService {
  async getAllCategories(): Promise<CategoryModel[]> {
    let data: { data: CategoryModel[] } = { data: [] as CategoryModel[] };
    await api
      .get("/categories/")
      .then((response: { data: CategoryModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
}

export default new CategoryDataService();
