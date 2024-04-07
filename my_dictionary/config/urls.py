from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("tinymce/", include("tinymce.urls")),
    path("admin/", admin.site.urls),
    path("", include("authentication.urls")),
    path("", include("dictionary.urls")),
    path("", include("articles.urls")),
    path("", include("diary.urls")),
    path("", include("feedback.urls")),
    path("", include("common.urls")),
    path("", include("text_books.urls")),
    path("", include("reader.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = "common.views.page_not_found_view"
handler500 = "common.views.server_error"

if not settings.DEBUG:
    urlpatterns += (
        re_path(
            r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}
        ),
    )
