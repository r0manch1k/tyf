import api from "@/stores/services/api";
import type ProfileListItemModel from "@/models/ProfileModel";
import type ProfileDetailModel from "@/models/ProfileModel";
import type PostListItemModel from "@/models/PostModel";

class ProfileDataService {
  async getMyProfile(): Promise<ProfileListItemModel> {
    let data: { data: ProfileListItemModel } = {
      data: {} as ProfileListItemModel,
    };
    await api
      .get("/profiles/me/")
      .then((response: { data: ProfileListItemModel }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }

  async getAllProfiles(): Promise<ProfileListItemModel[]> {
    let data: { data: ProfileListItemModel[] } = {
      data: [] as ProfileListItemModel[],
    };
    await api
      .get("/profiles/")
      .then((response: { data: ProfileListItemModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }

  async getProfileByUsername(username: string): Promise<ProfileDetailModel> {
    let data: { data: ProfileDetailModel } = { data: {} as ProfileDetailModel };
    await api
      .get(`/profiles/${username}/`)
      .then((response: { data: ProfileDetailModel }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }

  async getRecentProfiles(): Promise<ProfileListItemModel[]> {
    let data: { data: ProfileListItemModel[] } = {
      data: [] as ProfileListItemModel[],
    };
    await api
      .get("/profiles/recent/")
      .then((response: { data: ProfileListItemModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }

  async getMostActiveProfiles(): Promise<ProfileListItemModel[]> {
    let data: { data: ProfileListItemModel[] } = {
      data: [] as ProfileListItemModel[],
    };
    await api
      .get("/profiles/most-active/")
      .then((response: { data: ProfileListItemModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }

  async getProfilePosts(username: string): Promise<PostListItemModel[]> {
    let data: { data: PostListItemModel[] } = {
      data: [] as PostListItemModel[],
    };
    await api
      .get(`/profiles/${username}/posts/`)
      .then((response: { data: PostListItemModel[] }) => (data = response))
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
