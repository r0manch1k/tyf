from rest_framework import serializers
from .models import Media
from tyf import settings


# class MediaRelatedField(serializers.RelatedField):
#     def to_representation(self, value):
#         if isinstance(value, Media):
#             serializer = MediaSerializer(value)
#         else:
#             raise Exception("Unexpected type of tagged object")

#         return serializer.data


class MediaSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ["id", "file", "description", "original_filename"]

    def get_file(self, obj):
        return settings.API_ULR + obj.file.url
