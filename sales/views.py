from sales.models import Article, ArticleCategory, Sale
from sales.serializers import ArticleSerializer, ArticleCategorySerializer, SaleSerializer
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

class ArticleCategoryViewSet(ModelViewSet):
    queryset = ArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

# ViewSets define the view behavior.
class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]
