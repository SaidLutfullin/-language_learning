from django.contrib import admin
from .models import ServicePage
from .forms import ServicePageAdminForm


class ServicePageAdmin(admin.ModelAdmin):
    list_display = ('page_type', )
    list_filter = ('page_type', )
    search_fields = ('page_type', )
    form = ServicePageAdminForm

admin.site.register(ServicePage, ServicePageAdmin)