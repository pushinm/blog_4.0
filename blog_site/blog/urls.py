from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.decorators.http import condition
from .views import AllPAges, BlogDelete, BlogDetail, blog_update, add_comment, CreateBlog, \
    latest_entry

app_name = 'blog'

urlpatterns = [
    path('', AllPAges.as_view(), name='all_pages'),
    path('blogdetail-<int:pk>/', BlogDetail.as_view(),
         name='detail_page'),
    path('create/', CreateBlog.as_view(), name='create_blog'),
    path('blog/delete/<int:pk>/', BlogDelete.as_view(), name='delete_blog'),
    path('blog_add_comment/<int:pk>/', add_comment, name='add_comment'),
    path('update_all/', blog_update, name='update_all'),
]
