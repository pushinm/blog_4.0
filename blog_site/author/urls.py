from django.urls import path
from .views import AuthorDetail, CreateAuthor, CreateAuthorApi, AuthorView, AuthorLoginTemplate, LogoutView, AuthorLogoutAPIView

app_name = 'authors'

apiurls = [
    path('api/create_author/', CreateAuthorApi.as_view(), name='create_author_api'),
    path('api/logout/', AuthorLogoutAPIView.as_view(), name='author_logout'),
    path('authorview/', AuthorView.as_view(), name='authorview')
]

urlpatterns = [
    path('login/', AuthorLoginTemplate.as_view(), name='login_author'),
    path('logout/', LogoutView.as_view(), name='authorlogoutview'),
    path('create_author/', CreateAuthor.as_view(), name='create_author'),
    path('current/<int:pk>/', AuthorDetail.as_view(), name='author_detail')
]

urlpatterns += apiurls
