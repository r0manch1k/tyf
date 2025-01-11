import ProfileModel from "@/models/ProfileModel";
import api from "@/stores/services/api";

class ProfileDataService {
  async getAllProfiles(): Promise<ProfileModel[]> {
    let data: { data: ProfileModel[] } = { data: [] as ProfileModel[] };
    await api
      .get("/profiles/")
      .then((response: { data: ProfileModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }

  async getProfileByUsername(username: string): Promise<ProfileModel> {
    let data: { data: ProfileModel } = { data: {} as ProfileModel };
    await api
      .get(`/profiles/${username}/`)
      .then((response: { data: ProfileModel }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }

  async getRecentProfiles(): Promise<ProfileModel[]> {
    let data: { data: ProfileModel[] } = { data: [] as ProfileModel[] };
    await api
      .get("/profiles/recent/")
      .then((response: { data: ProfileModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }

  //   async createProfile(profile: ProfileModel): Promise<ProfileModel> {
  //     let data: { data: ProfileModel } = { data: {} as ProfileModel };
  //     await api
  //       .post("/profiles/", profile)
  //       .then((response: { data: ProfileModel }) => (data = response))
  //       .catch((error: unknown) => console.error(error));
  //     return data.data;
  //   }
}

export default new ProfileDataService();
