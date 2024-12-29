import api from "@/stores/services/api";
import CategoryModel from "@/models/CategoryModel";

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
