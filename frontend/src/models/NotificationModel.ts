export default interface NotificationModel {
  id: number;
  recipient: string;
  kind: string;
  text: string;
  read: boolean;
  target: string;
  created_at: string;
}
