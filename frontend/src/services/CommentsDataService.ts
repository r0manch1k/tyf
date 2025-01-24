import CommentModel from "@/models/CommentModel";
import api from "@/stores/services/api";


class CommentsDataService {
  async createComment(postId: string, comment: { content: string; author: number }): Promise<CommentModel> {
    console.log("Creating comment:", comment);
    try {
      const response = await api.post(`/posts/${postId}/comments/`, comment);
      return response.data;
    } catch (error) {
      console.error("Error creating comment:", error);
      throw error;
    }
  }
}

export default new CommentsDataService();
