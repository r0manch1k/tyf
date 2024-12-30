from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=Comment.objects.all(), widget=forms.HiddenInput, required=False
    )

    class Meta:
        model = Comment
        fields = (
            "content",
            "parent",
        )
        labels = {
            "content": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["content"].widget.attrs.update(
            {
                "class": "form-control comments__content",
                "placeholder": "Leave a comment",
            }
        )
