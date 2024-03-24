from rest_framework import serializers
from users.models import User
from .models import Article, ArticleCategory, Sale


class ArticleCategorySerializer(serializers.HyperlinkedModelSerializer):
    """Serialize of ArticleCategory model."""
    class Meta:
        model = ArticleCategory
        fields = '__all__'


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize of Article model."""
    class Meta:
        model = Article
        fields = '__all__'


class SaleSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize of Sale model."""
    article_code = serializers.SerializerMethodField()
    article_name = serializers.SerializerMethodField()
    article_category = serializers.SerializerMethodField()
    total_selling_price = serializers.SerializerMethodField()
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())

    class Meta:
        model = Sale
        fields = ['url',
                  'author',
                  'date',
                  'article',
                  'article_category',
                  'article_code',
                  'article_name',
                  'quantity',
                  'unit_selling_price',
                  'total_selling_price']
        read_only_fields = ['total_selling_price']

    def get_article_code(self, obj):
        return obj.article.code

    def get_article_name(self, obj):
        return obj.article.name

    def get_article_category(self, obj):
        return obj.article.category.display_name

    def get_total_selling_price(self, obj):
        return obj.get_total_selling_price()
