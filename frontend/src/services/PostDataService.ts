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
  count: number;
  next?: number;
  results: PostListItemModel[];
}

interface PostListParams {
  page: number;
  query?: string;
  search_method?: string;
}

interface PostListResult {
  count: number;
  posts: PostListItemModel[];
}

class PostDataService {
  async getPosts(query = "", searchMethod = ""): Promise<PostListResult> {
    let data: PostListResponse = {
      count: 0,
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

      let parameters: PostListParams = { page: currentPageId.value };
      if (query && searchMethod) {
        parameters = {
          ...parameters,
          query: query,
          search_method: searchMethod,
        };
      }

      await api
        .get("/posts/", {
          params: parameters,
        })
        .then((response: { data: PostListResponse }) => {
          data = response.data;

          if (!data.next) {
            store.commit("pagination/disablePostsFetching");
          }
        })
        .catch((error: unknown) => console.error(error));
    }
    return { posts: data.results, count: data.count };
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
