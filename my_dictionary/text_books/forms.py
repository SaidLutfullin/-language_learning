from django.forms import ModelForm
from django import forms
from tinymce.widgets import TinyMCE
from .models import TextBook, Exercise


class TextBookForm(ModelForm):
    class Meta:
        model = TextBook
        fields = ['name', 'description', 'book_file', 'keys_file', 'keys_page_number']

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
            "keys_page_number": forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            "name": "Название",
            "description": "Описание",
            "book_file": "Учебник (в формате pdf)",
            "keys_file": "Файл с ключами (в формате pdf)",
            "keys_page_number": "Страница, на которой начинаются ключи",
        }


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ['title', 'date', 'text', 'page_number', 'keys_page_number']

        widgets = {
            "date": forms.DateInput(format=('%Y-%m-%d'),
                                    attrs={'type': 'date',
                                           'class': 'form-control'}),
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "text": TinyMCE(),
            "page_number": forms.HiddenInput(),
            "keys_page_number": forms.HiddenInput(),
        }

        labels = {
            "title": "Заголовок",
            "date": "Дата",
            "text": "Текст",
        }
