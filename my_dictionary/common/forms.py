from django import forms

from .models import ServicePage


class ServicePageAdminForm(forms.ModelForm):
    class Meta:
        model = ServicePage
        fields = "__all__"
