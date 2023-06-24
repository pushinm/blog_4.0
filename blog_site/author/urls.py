from django.urls import path
from .views import AuthorDetail, CreateAuthor, CreateAuthorApi

app_name = 'authors'

urlpatterns = [
    path('create_author/', CreateAuthor.as_view(), name='create_author'),
    path('api/create_author/', CreateAuthorApi.as_view(), name='create_author_api'),
    path('current/<int:pk>/', AuthorDetail.as_view(), name='author_detail')
]
