from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Blog


class BlogMixin(View):
    model = Blog

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        context = {
            'blog': blog
        }
        return self.render_to_response(context)
