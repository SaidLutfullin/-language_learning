from django import forms
from .models import Diary
from tinymce.widgets import TinyMCE
from django.forms import ModelForm


class DiaryForm(ModelForm):
    class Meta:
        model = Diary
        fields = ['date', 'title', 'text']

        widgets = {
            "date": forms.DateInput(format=('%Y-%m-%d'),
                                    attrs={'type': 'date',
                                           'class': 'form-control w-25'}),
                                            
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "text": TinyMCE(attrs={'cols': 80, 'rows': 30})
        }
