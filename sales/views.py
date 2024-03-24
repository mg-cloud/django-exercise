from sales.models import Article, ArticleCategory, Sale
from sales.serializers import ArticleSerializer, ArticleCategorySerializer, SaleSerializer
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet


class ArticleCategoryViewSet(ModelViewSet):
    queryset = ArticleCategory.objects.all().order_by('display_name')
    serializer_class = ArticleCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all().order_by('code')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]


class SaleViewSet(ModelViewSet):
    # Order view by most recent sales
    queryset = Sale.objects.all().order_by('date').reverse()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]
