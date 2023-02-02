from django.urls import path
from .views import Articles, ShowArticle

urlpatterns = [
    path('', ShowArticle.as_view(), name='main'),
    path('articles/', Articles.as_view(), name='articles'),
    path('articles/<slug:article_slug>', ShowArticle.as_view(), name='show_article'),
]
