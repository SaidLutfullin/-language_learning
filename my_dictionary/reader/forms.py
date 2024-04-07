from django import forms
from django.forms import ModelForm

from reader.models import ForeignBook


class ForeignBookForm(ModelForm):
    class Meta:
        model = ForeignBook
        fields = ["title"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }
