from django import forms
from django.forms import ModelForm
from tinymce.widgets import TinyMCE

from diary.models import Diary


class DiaryForm(ModelForm):
    class Meta:
        model = Diary
        fields = ["date", "title", "text"]

        widgets = {
            "date": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"type": "date", "class": "form-control w-50"},
            ),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "text": TinyMCE(attrs={"cols": 80, "rows": 70}),
        }
