from django.urls import include, path, re_path
from rest_framework import routers

from .views import (ForeignBookCreateView, ForeignBookDeleteView,
                    ForeignBookListView, ForeignBookPageViewSet,
                    ForeignBooksChooseTypeDetailView, ForeignBookShow,
                    ForeignBookUpdateView, PDFBookCreateView,
                    PDFBookDeleteView, PDFBookListView, PDFBookRetrieveAPIView,
                    PDFBookSetPageNumberAPIView, PDFBookShow,
                    PDFBookUpdateView, TranslateAPIView)

router = routers.DefaultRouter()
router.register("foreign_book_page", ForeignBookPageViewSet)

urlpatterns = [
    path(
        "foreign_books_choose_type",
        ForeignBooksChooseTypeDetailView.as_view(),
        name="foreign_books_choose_type",
    ),
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
    path("PDFbooks", PDFBookListView.as_view(), name="PDFbook_list"),
    path("PDFbook/create", PDFBookCreateView.as_view(), name="PDFbook_create"),
    path(
        "PDFbook/<int:book_id>/update",
        PDFBookUpdateView.as_view(),
        name="PDFbook_update",
    ),
    path("PDFbook/<int:book_id>", PDFBookShow.as_view(), name="show_PDFbook"),
    path(
        "PDFbook/<int:book_id>/delete",
        PDFBookDeleteView.as_view(),
        name="PDFbook_delete",
    ),
    path("api/v1/PDFbook/<int:pk>", PDFBookRetrieveAPIView.as_view()),
    path(
        "api/v1/PDFbook_set_page_number/<int:pk>", PDFBookSetPageNumberAPIView.as_view()
    ),
]
