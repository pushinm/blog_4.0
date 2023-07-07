from rest_framework.serializers import ModelSerializer
from .models import Blog


class BlogsListSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'photo',)
