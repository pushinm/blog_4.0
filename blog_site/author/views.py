import datetime

from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from .models import Author
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth.models import User
from .forms import UserCreatingForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate, logout
from .forms import AuthAuthorForm
from django.http.response import HttpResponseBase, HttpResponseForbidden
from django.contrib import messages
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from .serializers import AuthorSerializer
from .models import Author
from rest_framework.permissions import AllowAny
from django.conf import settings
import jwt
from jwt import decode

# Create your views here.

class AuthorApiLogin(APIView):
    def post(self, request):
        username = request.data['username']
        print(username)
        print(request.data)
        password = request.data['password']
        print(password)
        author = Author.objects.filter(username=username).first()
        print(author)
        if author is None:
            raise AuthenticationFailed('Пользователь не найден')
        if not author.check_password(password):
            raise AuthenticationFailed('Неправильный пароль')

        payload = {
            'id': author.pk,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        # token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
        responce = Response()
        responce.set_cookie(key='jwt', value=token, httponly=True)
        responce.data = {
            'jwt': token
        }
        return responce

class AuthorView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('AuthenticationFailed')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('ExpiredSignatureError')

        author = Author.objects.filter(id=payload['id']).first()
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

class AuthorLogin(LoginView):
    template_name = 'logs/login.html'
    form_class = AuthAuthorForm
    success_url = reverse_lazy('blog:blog')

    def dispatch(self, request, *args, **kwargs):
        if 'user' in request.COOKIES:
            username = request.COOKIES['user']
            password = request.COOKIES['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                responce = HttpResponseForbidden(
                    "Вы уже сделали вход так как мы использовали куки. до этого вы регистрировались. вот мы и запомнили эти данные но ради безопасности сразу же удалили эти куки")
                responce.delete_cookie('user')
                responce.delete_cookie('password')
                return responce
        return super().dispatch(request, *args, **kwargs)


def create_render(request):
    return render(request, template_name='forms_and_reg/user_registration.html')


class CreateAuthorApi(CreateAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    # permission_classes = AllowAny

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     print()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #


class CreateAuthor(CreateView):
    form_class = UserCreatingForm
    template_name = 'forms_and_reg/user_registration.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = UserCreatingForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            logout(request)

            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], )
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            login(request, new_user)
            responce = redirect('/')
            responce.set_cookie('user', f'{username}')
            responce.set_cookie('password', f'{password}')
            return responce
        else:
            return render(request, self.template_name, {'form': form})


class AuthorDetail(DetailView):
    model = Author
    template_name = 'pages/author_detail.html'
    context_object_name = 'current_author'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('author_of_blog')

        return queryset
