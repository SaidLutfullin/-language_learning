from django import forms
from tinymce.widgets import TinyMCE

from .models import Article, Comment


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        exclude = ("preview",)

        widgets = {
            "text": TinyMCE(attrs={"cols": 80, "rows": 30}),
        }


class CommentForm(forms.ModelForm):
    agreement = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Comment
        fields = ("name", "email", "text")

        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Имя", "class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "E-mail", "class": "form-control"}
            ),
            "text": TinyMCE(attrs={"cols": 80, "rows": 30}),
        }
