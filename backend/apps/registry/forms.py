from django_select2 import forms as s2forms
from .models import Major, University


class UniversityWidget(s2forms.ModelSelect2Widget):
    queryset = University.objects.all().order_by("name")
    is_required = False
    search_fields = [
        "name__icontains",
        "city__icontains",
        "country__icontains",
    ]


class MajorWidget(s2forms.ModelSelect2Widget):
    queryset = Major.objects.all().order_by("name")
    is_required = False
    search_fields = [
        "name__icontains",
    ]
