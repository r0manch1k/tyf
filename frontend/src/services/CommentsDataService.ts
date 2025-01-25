import CreateCommentPayload from "@/models/CreateCommentPayload";
import api from "@/stores/services/api";


class CommentsDataService {
  async createComment(payload: CreateCommentPayload): Promise<void> {
    const { post } = payload;
    await api
      .post(`/posts/${post}/comments/`, payload)
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
