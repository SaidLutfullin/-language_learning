from django.urls import path

from .views import (AddingWord, CreateUpdateWordAPIView, Dictionary, EditWord,
                    Exporting, GetSuccessPage, TestView, WordOperations)

urlpatterns = [
    path("dictionary/", Dictionary.as_view(), name="dictionary"),
    path("adding_word", AddingWord.as_view(), name="adding_word"),
    path("test", TestView.as_view(), {"question_type": "test"}, name="test"),
    path("cards", TestView.as_view(), {"question_type": "cards"}, name="cards"),
    path("edit/", EditWord.as_view(), name="edit"),
    path("export/", Exporting.as_view(), name="export"),
    path(
        "api/v1/word_operations", WordOperations.as_view(), name="word_operations_api"
    ),
    path(
        "api/v1/get_success_page", GetSuccessPage.as_view(), name="get_success_page_api"
    ),
    path("api/v1/add_word", CreateUpdateWordAPIView.as_view(), name="adding_word_api"),
    path(
        "api/v1/update_word/<int:pk>",
        CreateUpdateWordAPIView.as_view(),
        name="updating_word_api",
    ),
]
