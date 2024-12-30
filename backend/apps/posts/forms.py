from django import forms
from .models import Post
from apps.registry.models import Major, University
from apps.registry.forms import MajorWidget, UniversityWidget
from apps.profiles.models import Profile


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class PostForm(forms.ModelForm):
    media_files = MultipleFileField(required=False)
    tags = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "tags",
            "content",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update(
            {
                "placeholder": "Title",
            }
        )

        self.fields["tags"].widget.attrs.update(
            {
                "placeholder": "math,science,etc",
            }
        )


class EditProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    avatar = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control-file"})
    )

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
    )

    university = forms.ModelChoiceField(
        queryset=University.objects.all().order_by("name"),
        required=False,
    )

    major = forms.ModelChoiceField(
        queryset=Major.objects.all().order_by("name"),
        required=False,
    )

    autocomplete_fields = [
        "university",
        "major",
    ]

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "middle_name",
            "university",
            "major",
            "date_of_birth",
            "bio",
            "avatar",
            "telegram",
            "vkontakte",
        ]
        widgets = {
            "university": UniversityWidget,
            "major": MajorWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update(
            {
                "placeholder": "Ivan",
            }
        )

        self.fields["last_name"].widget.attrs.update(
            {
                "placeholder": "Ivanov",
            }
        )

        self.fields["middle_name"].widget.attrs.update(
            {
                "placeholder": "Ivanovich",
            }
        )

        self.fields["telegram"].widget.attrs.update(
            {
                "placeholder": "https://t.me/username",
            }
        )

        self.fields["vkontakte"].widget.attrs.update(
            {
                "placeholder": "https://vk.com/username",
            }
        )

        self.fields["bio"].widget.attrs.update(
            {
                "placeholder": "Tell your friends about yourself",
            }
        )
