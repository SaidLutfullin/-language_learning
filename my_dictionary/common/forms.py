from .models import ServicePage
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms

class ServicePageAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="extends"))
    
    class Meta:
        model = ServicePage
        fields = "__all__"