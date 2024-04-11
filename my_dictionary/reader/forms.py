from django import forms
from django.forms import ModelForm

from reader.models import ForeignBook, PDFBook


class ForeignBookForm(ModelForm):
    class Meta:
        model = ForeignBook
        fields = [
            "title",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }


class PDFBookForm(ModelForm):
    class Meta:
        model = PDFBook
        fields = ["title", "book_file"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }

        labels = {
            "title": "Название",
            "book_file": "Файл (в формате pdf)",
        }
