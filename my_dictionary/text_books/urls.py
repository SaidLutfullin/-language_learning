from django.urls import path
from . import views

urlpatterns = [
    path('text_books', views.TextBooksList.as_view(), name='my_text_books'),
    path('text_books/<int:text_book_id>', views.ShowTextBook.as_view(), name='show_text_book'),
    path('text_books/<int:text_book_id>/edit', views.EditTextBook.as_view(), name='edit_text_book'),
    path('text_books/<int:text_book_id>/delete', views.DeleteTextBook.as_view(), name='delete_text_book'),

    path('text_books/add', views.AddTextBook.as_view(), name='add_text_book'),
    path('text_books/<int:text_book_id>/add_exercise', views.AddExercise.as_view(), name='add_exercise'),
    path('text_books/exercise/<int:exercise_id>', views.UpdateExercise.as_view(), name='update_exercise'),
    path('text_books/exercise/<int:exercise_id>/delete', views.DeleteExercise.as_view(), name='delete_exercise'),

]
