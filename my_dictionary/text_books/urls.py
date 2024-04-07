from django.urls import include, path
from rest_framework import routers

from text_books.views import (AddTextBook, DeleteTextBook, EditTextBook,
                              ExerciseViewSet, TextBookManager,
                              TextBookRetrieveAPIView, TextBooksList)

router = routers.DefaultRouter()

router.register("exercises", ExerciseViewSet)


urlpatterns = [
    path("text_books", TextBooksList.as_view(), name="my_text_books"),
    path(
        "text_books/<int:text_book_id>",
        TextBookManager.as_view(),
        name="show_text_book",
    ),
    path(
        "text_books/<int:text_book_id>/edit",
        EditTextBook.as_view(),
        name="edit_text_book",
    ),
    path(
        "text_books/<int:text_book_id>/delete",
        DeleteTextBook.as_view(),
        name="delete_text_book",
    ),
    path("text_books/add", AddTextBook.as_view(), name="add_text_book"),
    path("api/v1/", include(router.urls)),
    path("api/v1/text_books/<int:pk>", TextBookRetrieveAPIView.as_view()),
]
