from django.urls import path, include

from rest_framework import routers
from users.views import UserViewSet
from sales.views import ArticleViewSet, ArticleCategoryViewSet, SaleViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'article', ArticleViewSet)
router.register(r'articlecategory', ArticleCategoryViewSet)
router.register(r'sales', SaleViewSet)
urlpatterns = [
    path(
        "v1/",
        include(
            [
                path("", include(router.urls)),
            ]
        ),
    )
]
