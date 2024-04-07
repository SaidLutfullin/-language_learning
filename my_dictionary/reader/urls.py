from django.urls import include, path, re_path
from rest_framework import routers

from .views import (ForeignBookCreateView, ForeignBookDeleteView,
                    ForeignBookListView, ForeignBookPageViewSet,
                    ForeignBookShow, ForeignBookUpdateView, TranslateAPIView)

router = routers.DefaultRouter()
router.register("foreign_book_page", ForeignBookPageViewSet)

urlpatterns = [
    path("foreing_books", ForeignBookListView.as_view(), name="foreign_books"),
    path(
        "foreing_books/create",
        ForeignBookCreateView.as_view(),
        name="foreign_books_create",
    ),
    path(
        "foreing_books/<int:book_id>/update",
        ForeignBookUpdateView.as_view(),
        name="foreign_books_update",
    ),
    path(
        "foreing_books/<int:book_id>/delete",
        ForeignBookDeleteView.as_view(),
        name="foreign_books_delete",
    ),
    re_path(
        r"^foreing_books/(?P<book_id>\d+)/(?:.*)$",
        ForeignBookShow.as_view(),
        name="show_foreign_book",
    ),
    path("api/v1/", include(router.urls)),
    path("api/v1/translate", TranslateAPIView.as_view(), name="translate"),
]
