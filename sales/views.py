from django.db.models import F, FloatField, Sum, Max, Value, DateField
from django.db.models.functions import Concat
from rest_framework import permissions, generics
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from sales.models import Article, ArticleCategory, Sale
from sales.serializers import ArticleSerializer, ArticleCategorySerializer, SaleSerializer, AggregatedSaleSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Sale-level permission to only allow author of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # If request is read only, allow it
        if request.method in permissions.SAFE_METHODS:
            return True
        # Else check that the user is the author of the sale
        return obj.author == request.user


class ArticleCategoryViewSet(ModelViewSet):
    """Article Category ViewSet."""
    queryset = ArticleCategory.objects.all().order_by('display_name')
    serializer_class = ArticleCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ArticleViewSet(ModelViewSet):
    """Article ViewSet."""
    queryset = Article.objects.all().order_by('code')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]


class SaleViewSet(ModelViewSet):
    """Sale Category ViewSet."""
    # Order view by most recent sales
    queryset = Sale.objects.order_by('date').reverse()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class AggregatedSaleViewSet(ReadOnlyModelViewSet):
    """Aggregated Sale by Article ViewSet."""
    serializer_class = AggregatedSaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Use prefetch_related to avoid a db call for each sale's article and article category
        return Sale.objects.prefetch_related("article", "article__category").values("article").annotate(
                                            category=F('article__category'),
                                            sales_total_revenue=Sum(F('quantity') * F('unit_selling_price')),
                                            margin=Sum((F('unit_selling_price') - F('article__manufacturing_cost')) * F('quantity')),
                                            last_sale_date=Max('date')
                                            ).order_by("sales_total_revenue").reverse()
