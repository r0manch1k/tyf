import type { ProfileDetailModel } from "@/models/ProfileModel";
import type { ProfileListItemModel } from "@/models/ProfileModel";
import type { PostListItemModel } from "@/models/PostModel";
import type { ChatListItemModel } from "@/models/ChatModel";
import api from "@/stores/services/api";
import store from "@/stores";

class ProfileDataService {
  async getMyProfile(): Promise<ProfileListItemModel | void> {
    let data: { data: ProfileListItemModel } = {
      data: {} as ProfileListItemModel,
    };
    await api
      .get("/profiles/me/")
      .then((response) => {
        if (response.status === 200) {
          data = response;
        } else {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
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
      .catch((error: unknown) => console.error(error, "Profile"));
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

  async getProfileFollowers(username: string): Promise<ProfileListItemModel[]> {
    let data: { data: ProfileListItemModel[] } = {
      data: [] as ProfileListItemModel[],
    };
    await api
      .get(`/profiles/${username}/followers/`)
      .then((response: { data: ProfileListItemModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }

  async getProfileFollowing(username: string): Promise<ProfileListItemModel[]> {
    let data: { data: ProfileListItemModel[] } = {
      data: [] as ProfileListItemModel[],
    };
    await api
      .get(`/profiles/${username}/following/`)
      .then((response: { data: ProfileListItemModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }

  async followProfile(username: string): Promise<void> {
    await api
      .post(`/profiles/${username}/follow/`)
      .then((response) => {
        if (response.status === 200) {
          console.log("ProfileDataService.ts", response.data.payload);
        } else {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }
  async updateProfile(data: ProfileDetailModel): Promise<void> {
    const username = store.getters["profile/getProfile"].username;
    await api
      .patch(`/profiles/${username}/`, data)
      .then((response) => {
        if (response.status != 200) {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }

  async updateAvatar(file: File): Promise<void> {
    const username = store.getters["profile/getProfile"].username;
    const data = new FormData();
    data.append("avatar", file);
    await api
      .patch(`/profiles/${username}/avatar/`, data, {
        headers: {
          "content-type": "multipart/form-data",
        },
      })
      .then((response) => {
        if (response.status != 200) {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }

  async getProfileChats(username: string): Promise<ChatListItemModel[]> {
    let data: { data: ChatListItemModel[] } = {
      data: [] as ChatListItemModel[],
    };
    await api
      .get(`/profiles/${username}/chats/`)
      .then((response: { data: ChatListItemModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
}

export default new ProfileDataService();
