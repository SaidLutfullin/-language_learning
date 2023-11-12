from django.contrib import admin

from .forms import ServicePageAdminForm
from .models import ServicePage


class ServicePageAdmin(admin.ModelAdmin):
    list_display = ("page_type",)
    list_filter = ("page_type",)
    search_fields = ("page_type",)
    form = ServicePageAdminForm


admin.site.register(ServicePage, ServicePageAdmin)
