from django.urls import path
from . import views
from .views import get_comments_for_article, create_comment, delete_comment

urlpatterns = [
    path('<int:movie_id>/', views.get_articles_by_movie, name='movie-articles'),
    path('create/', views.create_article, name='create-article'),
    path('<int:article_id>/detail/', views.get_article, name='article-detail'),
    path('<int:article_id>/delete/', views.delete_article, name='delete-article'),
    path('<int:article_id>/update/', views.update_article, name='update-article'),
    path('<int:article_id>/comments/', get_comments_for_article, name='article-comments'),
    path('<int:article_id>/comment/create/', create_comment, name='create-comment'),
    path('<int:comment_id>/comment/delete/', delete_comment, name='delete-comment'),
    path('<int:comment_id>/comment/update/', views.update_comment, name='update-comment')
]
