import type UniversityModel from "@/models/UniversityModel";
import type MajorModel from "@/models/MajorModel";
import api from "@/stores/services/api";

class RegistryDataService {
  async getAllUniversities(): Promise<UniversityModel[]> {
    let data: { data: UniversityModel[] } = {
      data: [] as UniversityModel[],
    };
    await api
      .get("/universities/")
      .then((response: { data: UniversityModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
  async getAllMajors(): Promise<MajorModel[]> {
    let data: { data: MajorModel[] } = {
      data: [] as MajorModel[],
    };
    await api
      .get("/majors/")
      .then((response: { data: MajorModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
}

export default new RegistryDataService();
