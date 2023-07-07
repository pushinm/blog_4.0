import datetime

from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from .models import Author
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView
from django.contrib.auth.models import User
from .forms import UserCreatingForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate, logout
from .forms import AuthAuthorForm
from django.http.response import HttpResponseBase, HttpResponseForbidden
from django.contrib import messages
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from .serializers import AuthorSerializer, AuthorLoginSerializer, AuthorSerializer
from .models import Author
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import jwt
from jwt import decode


# Create your views here.

class LogoutView(TemplateView):
    template_name = 'logs/logout.html'


class AuthorView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorSerializer

    def get_object(self):
        return self.request.user


class AuthorLoginTemplate(TemplateView):
    template_name = 'logs/login.html'


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


class CreateAuthor(TemplateView):
    template_name = 'forms_and_reg/user_registration.html'


class AuthorDetail(DetailView):
    model = Author
    template_name = 'pages/author_detail.html'
    context_object_name = 'current_author'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('author_of_blog')

        return queryset


class AuthorView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed('AuthenticationFailed')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('ExpiredSignatureError')

        author = Author.objects.filter(id=payload['id']).first()
        serializer = AuthorSerializer(author)
        return Response(serializer.data)


class AuthorApiLogin(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        author = Author.objects.filter(username=username).first()
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
        if request.COOKIES.get('jwt'):
            responce.delete_cookie('jwt')
            print('Deleted')
        responce.set_cookie(key='jwt', value=token, httponly=True)
        responce.data = {
            'jwt': token
        }
        print(responce.data)
        return responce


class AuthorLogoutAPIView(GenericAPIView):
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        try:
            jwt = request.COOKIES.get('jwt')
            print(jwt)
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('jwt')
            return response
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateAuthorApi(CreateAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            response.delete_cookie('jwt')
            return response
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#
# class CreateAuthorApi(GenericAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = AuthorSerializer
#
#     def post(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             user = serializer.save()
#             token = RefreshToken.for_user(user)
#             data = serializer.data
#             data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
#             response = Response(data, status=status.HTTP_201_CREATED)
#             response.set_cookie(key='jwt', value={"refresh": str(token), "access": str(token.access_token)},
#                                 httponly=True)
#         except Exception as e:
#             print(e)
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
# class AuthorApiLogin(GenericAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = AuthorLoginSerializer
#
#     def post(self, request, *args, **kwargs):
#         print(request.data)
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             user = serializer.validated_data
#             serializer = AuthorSerializer(user)
#             token = RefreshToken.for_user(user)
#             data = serializer.data
#             data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
#
#             response = Response(data, status=status.HTTP_200_OK)
#             response.set_cookie(key='refresh', value=str(token))
#             return response
#         except Exception as e:
#             print(e)
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
