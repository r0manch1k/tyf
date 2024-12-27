import api from "@/stores/services/api";
import ProfileModel from "@/models/ProfileModel";

class ProfileDataService {
  async getStatic(): Promise<string> {
    let data: { data: string } = { data: "" };
    // TODO: If you need more static data except avatar, i think it's better to create a new store module for static data
    await api
      .get("/profiles/avatar/")
      .then((response: { data: string }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }

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
