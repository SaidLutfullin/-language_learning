from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Language, Words


class LanguageAdminForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ("language_name",)

        widgets = {
            "language_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class Exporting(forms.Form):
    russian_word = forms.BooleanField(
        label="Русское слово",
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    foreign_word = forms.BooleanField(
        label="Перевод",
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    context = forms.BooleanField(
        label="Контекст",
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    box_number = forms.BooleanField(
        label="Номер коробки",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    asking_date = forms.BooleanField(
        label="Дата ближайшего повторения",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
