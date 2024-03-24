from rest_framework import serializers
from .models import Article, ArticleCategory, Sale

class ArticleCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = '__all__'

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class SaleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'
