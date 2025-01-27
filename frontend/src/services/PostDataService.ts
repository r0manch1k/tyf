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

class PostDataService {
  async getPosts(
    query = "",
    searchMethod = ""
  ): Promise<{ posts: PostListItemModel[]; count: number }> {
    let data = {
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

      let parameters: { page: number; query?: string; search_method?: string } =
        {
          page: currentPageId.value,
        };

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
        .then(
          (response: {
            data: {
              count: number;
              results: PostListItemModel[];
              next?: number;
            };
          }) => {
            data = response.data;
            if (!response.data.next) {
              store.commit("pagination/disablePostsFetching");
            }
          }
        )
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

  async getMostCommentedPosts(): Promise<PostListItemModel[]> {
    let data: { data: PostListItemModel[] } = {
      data: [] as PostListItemModel[],
    };
    await api
      .get("/posts/most-commented/")
      .then((response: { data: PostListItemModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
  
  async getMostBookmarkedPosts(): Promise<PostListItemModel[]> {
    let data: { data: PostListItemModel[] } = {
      data: [] as PostListItemModel[],
    };
    await api
      .get("/posts/most-bookmarked/")
      .then((response: { data: PostListItemModel[] }) => (data = response))
      .catch((error: unknown) => console.error(error));
    return data.data;
  }
}

export default new PostDataService();
