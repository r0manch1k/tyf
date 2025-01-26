from rest_framework import serializers
from .models import Major, University


class MajorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = "__all__"


class UniversityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"
