from django import forms
from django.forms import ModelForm

from text_books.models import TextBook


class TextBookForm(ModelForm):
    class Meta:
        model = TextBook
        fields = ["name", "description", "book_file", "keys_file", "keys_page_number"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "keys_page_number": forms.NumberInput(attrs={"class": "form-control"}),
        }

        labels = {
            "name": "Название",
            "description": "Описание",
            "book_file": "Учебник (в формате pdf)",
            "keys_file": "Файл с ключами (в формате pdf)",
            "keys_page_number": "Страница, на которой начинаются ключи",
        }
