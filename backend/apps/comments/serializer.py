from rest_framework import serializers
from .models import Comment
from apps.media.serializer import MediaSerializer
from apps.profiles.models import Profile


class FilterCommentSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super(FilterCommentSerializer, self).to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


# class CommentSerializer(serializers.ModelSerializer):
#     media = MediaSerializer(many=True)
#     replies = RecursiveSerializer(many=True)
#     created_at = serializers.DateTimeField(
#         format="%Y-%m-%d %H:%M:%S",
#         input_formats=[
#             "%d.%m.%Y",
#             "iso-8601",
#         ],
#     )
#     updated_at = serializers.DateTimeField(
#         format="%Y-%m-%d %H:%M:%S",
#         input_formats=[
#             "%d.%m.%Y",
#             "iso-8601",
#         ],
#     )
#
#     def get_replies(self, obj):
#         return CommentSerializer(obj.replies.all(), many=True).data
#
#     def get_media(self, obj):
#         media = obj.media.all()
#         return MediaSerializer(media, many=True).data
#
#     def get_author(self, obj):
#         return obj.author.user.username
#
#     def get_post(self, obj):
#         return obj.post.identifier
#
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response["author"] = instance.author.user.username
#         response["post"] = instance.post.identifier
#         response["replies"] = CommentSerializer(instance.replies.all(), many=True).data
#         return response
#
#     def create(self, validated_data):
#         post = validated_data.pop("post")
#         author = validated_data.pop("author")
#         parent = validated_data.pop("parent", None)
#         media = validated_data.pop("media", [])
#
#         comment = Comment.objects.create(post=post, author=author, parent=parent, **validated_data)
#
#         for m in media:
#             comment.media.add(m)
#
#         return comment
#
#
#
#
#     class Meta:
#         model = Comment
#         list_serializer_class = FilterCommentSerializer
#         fields = [
#             "identifier",
#             "content",
#             "stars",
#             "created_at",
#             "updated_at",
#             "active",
#             "media",
#             "post",
#             "author",
#             "parent",
#             "replies",
#         ]
class CommentSerializer(serializers.ModelSerializer):
    print("CommentSerializer")
    media = MediaSerializer(many=True, read_only=True)
    replies = RecursiveSerializer(many=True, read_only=True)
    post = serializers.SerializerMethodField()
    # author = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    # author = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True)

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    parent = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Comment
        list_serializer_class = FilterCommentSerializer
        fields = [
            "identifier",
            "content",
            "stars",
            "created_at",
            "updated_at",
            "active",
            "media",
            "post",
            "author",
            "parent",
            "replies",
        ]

    def get_post(self, obj):
        return obj.post.identifier

    def get_author(self, obj):
        return obj.author.username

    def to_representation(self, instance):
        print(f"Representing comment: {instance}")
        response = super().to_representation(instance)
        response["author"] = instance.author.username
        response["parent"] = instance.parent.identifier if instance.parent else None
        return response

    def create(self, validated_data):
        print("create start")
        post = validated_data.pop("post")
        author = validated_data.pop("author", None)

        if not author:
            author = self.context["request"].user.profile

        if not isinstance(author, Profile):
            raise ValueError("Invalid author provided")

        parent_identifier = validated_data.get("parent", None)
        parent = None
        if parent_identifier:
            if isinstance(parent_identifier, str):
                parent = Comment.objects.get(identifier=parent_identifier)
                validated_data["parent"] = parent
            else:
                raise serializers.ValidationError("Parent identifier must be a string.")
        print(f"Parent in create: {parent}")

        media = validated_data.pop("media", [])

        comment = Comment.objects.create(post=post, author=author, **validated_data)

        if media:
            comment.media.add(*media)

        return comment
