import api from "@/stores/services/api";
import type TyeUserModel from "@/tye_frontend/models/TyeUserModel";

class TyeDataService {
  async getHighscores(): Promise<TyeUserModel[]> {
    const response = await api.get("/tye/leaderboard/");
    return response.data as TyeUserModel[];
  }
}

export default new TyeDataService();
