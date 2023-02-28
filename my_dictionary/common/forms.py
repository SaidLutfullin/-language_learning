from .models import ServicePage
from django import forms


class ServicePageAdminForm(forms.ModelForm):

    class Meta:
        model = ServicePage
        fields = "__all__"
