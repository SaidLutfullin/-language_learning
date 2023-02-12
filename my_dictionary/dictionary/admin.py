from django.contrib import admin
from .models import Language
from .forms import LanguageAdminForm


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language_name', )
    list_display_links = ('language_name',)
    search_fields = ('language_name', )
    form = LanguageAdminForm
    list_filter = ('language_name', )

admin.site.register(Language, LanguageAdmin)
