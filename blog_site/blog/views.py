from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView, DetailView, FormView, UpdateView, CreateView, TemplateView
from testimonials.models import Testimonial
from django.contrib import messages
from testimonials.models import Testimonial
from .models import Blog
from .forms import BlogCreationForm
from django.forms import modelformset_factory
from testimonials.forms import CommentForm
from author.models import Author
from icecream import ic
from django.db import transaction
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.conf import settings
from django.utils.decorators import method_decorator
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page, cache_control
from django.views.decorators.http import condition, etag, last_modified
from django.utils import timezone
from .CustomMixins import BlogMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from rest_framework.generics import ListAPIView
from .serializers import BlogsListSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class BlogsPagination(PageNumberPagination):
    page_size = 2


def latest_entry(request, pk):
    pub_date = Blog.objects.filter(pk=pk).first()
    return pub_date.published_at


def get_last_modified(request, *args, **kwargs):
    return timezone.now()


def get_etag(request, *args, **kwargs):
    etag = request.get_full_path() + str(timezone.now())
    # etag = '1234455514544'
    return etag


@method_decorator(cache_control(max_age=0), name='dispatch')
class CreateBlog(CreateView, SuccessMessageMixin):
    model = Blog
    form_class = BlogCreationForm
    template_name = 'pages/blog_create.html'
    success_url = '/'
    success_message = f'Создана новая статья'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        if self.success_message:
            messages.success(self.request, self.success_message)
            cache.delete('all_pages')
        form.save()
        return super().form_valid(form)


class AllBlogsTemplate(TemplateView):
    template_name = 'pages/all_pages.html'


class AllBlogsAPi(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogsListSerializer
    pagination_class = BlogsPagination


@method_decorator(cache_page(timeout=120, key_prefix='detail_blog'), name='get')
class BlogDetail(BlogMixin, TemplateView):
    template_name = 'pages/page_detail.html'
    context_object_name = 'blog'


class BlogDelete(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'pages/page_detail.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        blog = self.get_object()
        if request.user != blog.author:
            return render(request, self.template_name)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        comments = blog.blog_of_tes.all()
        print(comments)
        comments.delete()
        return super().delete(request, *args, **kwargs)


def blog_update(request):
    BlogFormSet = modelformset_factory(Blog, fields='__all__')
    if request.method == 'POST':
        formset = BlogFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Статья исправлена')
            return redirect('/')
    else:
        formset = BlogFormSet()
    context = {
        'formset': formset
    }
    return render(request=request, template_name='pages/page_edit.html', context=context)


def add_comment(request, pk):
    template_name = 'pages/page_detail.html'
    blog = Blog.objects.get(pk=pk)
    if request.method == 'POST':
        text = request.POST.get('message')
        print(text)
        Testimonial.objects.create(testimonial=text, blog=blog)
        return redirect(f'/blogdetail-{blog.pk}/')
    return render(request=request, template_name=template_name, context={'text': '1'})
