import type {
  default as PostDetailModel,
  default as PostListItemModel,
} from "@/models/PostModel";
import store from "@/stores";
import api from "@/stores/services/api";
import { ref } from "vue";
// import type CategoryModel from "@/models/CategoryModel";
// import type CollectionModel from "@/models/CollectionModel";
// import type TagModel from "@/models/TagModel";
// import type ProfileModel from "@/models/ProfileModel";
// import PostDetailView from "@/views/PostDetailView.vue";

interface PostListResponse {
  results: PostListItemModel[];
  next?: number;
}

class PostDataService {
  async getPosts(): Promise<PostListItemModel[]> {
    let data: PostListResponse = {
      results: [] as PostListItemModel[],
    };

    const fetchingPostsStatus = ref<boolean>(
      store.getters["pagination/getFetchingStatus"]
    );

    if (fetchingPostsStatus.value) {
      store.commit("pagination/incrementPostsPage");
      const currentPageId = ref<number>(
        store.getters["pagination/getCurrentPostsPage"]
      );

      await api
        .get("/posts/", {
          params: {
            page: currentPageId.value,
          },
        })
        .then((response: { data: { results: PostListItemModel[] } }) => {
          data = response.data;

          if (!data.next) {
            store.commit("pagination/disablePostsFetching");
          }
        })
        .catch((error: unknown) => console.error(error));
    }
    return data.results;
  }

  async getPostByIdentifier(identifier: string): Promise<PostDetailModel> {
    let data: { data: PostDetailModel } = { data: {} as PostDetailModel };
    await api
      .get(`/posts/${identifier}`)
      .then((response: { data: PostDetailModel }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
}

export default new PostDataService();
