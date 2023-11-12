from django import forms
from django.forms import ModelForm
from tinymce.widgets import TinyMCE

from .models import Contact


class ContactForm(ModelForm):
    agreement = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Contact
        fields = "__all__"

        labels = {"name": "Имя", "email": "E-mail", "message": "Сообщение"}

        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Имя", "class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "E-mail", "class": "form-control"}
            ),
            "message": TinyMCE(
                attrs={"placeholder": "Сообщение", "class": "form-control"}
            ),
        }
