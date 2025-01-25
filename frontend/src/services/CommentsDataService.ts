import CreateCommentPayload from "@/models/CreateCommentPayload";
import api from "@/stores/services/api";


class CommentsDataService {
  async createComment(payload: CreateCommentPayload): Promise<void> {
    const { post, ...rest } = payload;
    console.log("CommentsDataService.createComment", post, rest);
    await api
      .post(`/posts/${post}/comments/`, rest)
      .then((response) => {
        if (response.status !== 201) {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }
}

export default new CommentsDataService();
