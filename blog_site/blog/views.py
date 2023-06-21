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
from django.views.decorators.cache import cache_page
from django.views.decorators.http import condition, etag, last_modified
from django.utils import timezone
from .CustomMixins import BlogMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def latest_entry(request, pk):
    pub_date = Blog.objects.filter(pk=pk).first()
    return pub_date.published_at


def get_last_modified(request, *args, **kwargs):
    return timezone.now()


def get_etag(request, *args, **kwargs):
    # etag = request.get_full_path()+str(timezone.now())
    etag = '1234455514544'
    return etag


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
        form.save()
        return super().form_valid(form)


# @method_decorator(cache_page(CACHE_TTL), name='dispatch')
# @method_decorator(last_modified(get_last_modified), name='dispatch')
# @method_decorator(etag(get_etag), name='dispatch')
class AllPAges(ListView, HttpResponse):
    model = Blog
    template_name = 'pages/all_pages.html'
    context_object_name = 'blogs'
    paginate_by = 4

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['authors'] = Author.objects.all()
        return context


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
            messages.error(request, "You don't have permission to delete this blog.")
            return render(request, self.template_name)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        comments = blog.blog_of_tes.all()
        print(comments)
        comments.delete()
        messages.success(request, "Blog deleted successfully.")
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
        # return render(request=request, template_name=template_name, context={'text': text})
    return render(request=request, template_name=template_name, context={'text': '1'})

# def delete_article(request, pk):
#     article = get_object_or_404(Blog, pk=pk)
#     print(article)
#     if request.method == 'GET' and request.user == article.author:
#         return article.delete()
#
#
# def delete_comments(request, pk):
#     article = get_object_or_404(Blog, pk=pk)
#     comments = article.blog_of_tes.all()
#     print(comments)
#     if request.method == 'GET':
#         return comments.delete()
#     # ic(article)
#     # ic(comments)
#
#
# @transaction.atomic
# def delete_blog_with_comments(request, pk):
#     delete_comments(request, pk)
#     delete_article(request, pk)
#     return redirect('/')
