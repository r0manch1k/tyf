import CommentPayload from "@/models/CommentPayload";
import api from "@/stores/services/api";
import { AxiosResponse } from "axios"

class CommentsDataService {
  // async createComment(payload: CreateCommentPayload): Promise<any> {
  //   const { post, ...rest } = payload;
  //   console.log("CommentsDataService.createComment", post, rest);
  //   await api
  //     .post(`/posts/${post}/comments/`, rest)
  //     .then((response) => {
  //       if (response.status === 201) {
  //         return response.data;
  //       } else {
  //         return Promise.reject(response);
  //       }
  //
  //     })
  //     .catch((error) => {
  //       return Promise.reject(error);
  //     });
  // }

  async createComment(payload: CommentPayload): Promise<AxiosResponse> {
    const { post, ...rest } = payload;
    console.log("CommentsDataService.createComment", post, rest);

    return api
      .post(`/posts/${post}/comments/`, rest)
      .then((response) => {
        if (response.status === 201) {
          return response.data;
        } else {
          return Promise.reject(
            `Unexpected response status: ${response.status}`
          );
        }
      })
      .catch((error) => {
        console.error("Error creating comment:", error);
        return Promise.reject(error);
      });
  }

  async deleteCommentByIdentifier(identifier: string): Promise<void> {
    await api
      .delete(`/comments/${identifier}/`)
      .then((response) => {
        if (response.status !== 204) {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }

  // TODO: sort comments by created date 
  async updateCommentByIdentifier(
    identifier: string,
    payload: CommentPayload
  ): Promise<void> {
    await api
      .patch(`/comments/${identifier}/`, payload)
      .then((response) => {
        if (response.status !== 200) {
          return Promise.reject(response);
        }
      })
      .catch((error) => {
        return Promise.reject(error);
      });
  }

  async createReply(payload: CommentPayload): Promise<AxiosResponse> {
    const { post, ...rest } = payload;
    console.log("CommentsDataService.createReply", post, rest);

    return api
      .post(`/posts/${post}/comments/`, rest)
      .then((response) => {
        if (response.status === 201) {
          return response.data;
        } else {
          return Promise.reject(
            `Unexpected response status: ${response.status}`
          );
        }
      })
      .catch((error) => {
        console.error("Error creating reply:", error);
        return Promise.reject(error);
      });
  }
}

export default new CommentsDataService();
