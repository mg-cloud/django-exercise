from django.urls import reverse_lazy
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
    author = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail')
    article = serializers.HyperlinkedRelatedField(queryset=Article.objects.all(), view_name='article-detail')

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


class AggregatedSaleSerializer(serializers.ModelSerializer):
    """Serialize of Sale aggregated."""

    class Meta:
        model = Sale
        fields = '__all__'

    def to_representation(self, instance):
        """Override representation to give a more detailed view of the aggregated sale:
            - article url : link to the article
            - category url : link to the article category
            - sales_total_revenue : total revenue from sales
            - margin : sales_total_revenue - manufacturing_cost
            - last_sale_date"""
        return {
                "article": self.context['request'].build_absolute_uri(reverse_lazy("article-detail", args=[instance['article']])),
                # "category": instance['category'],
                "category": self.context['request'].build_absolute_uri(reverse_lazy("articlecategory-detail", args=[instance['category']])),
                # round to 2 decimals as it's most of the time the currency decimal place
                "sales_total_revenue": round(instance["sales_total_revenue"], 2),
                "margin": round(instance["margin"], 2),
                "last_sale_date": instance['last_sale_date'],
            }
