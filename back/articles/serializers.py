from rest_framework import serializers
from .models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id', 'author', 'author_username', 'content', 'rank', 'movie', 'created_at', 'updated_at']

    def get_author_username(self, obj):
        return obj.author.username


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_username', 'content', 'created_at', 'updated_at']

    def get_author_username(self, obj):
        return obj.author.username