export default interface CommentPayload {
  content: string;
  post: string;
  parent?: number | null;
}
