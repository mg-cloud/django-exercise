from django.urls import path, include

from rest_framework import routers
from users.views import UserViewSet
from sales.views import ArticleViewSet, ArticleCategoryViewSet, SaleViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', UserViewSet, basename='user')
router.register(r'sale', SaleViewSet, basename='sale')
router.register(r'article', ArticleViewSet, basename='article')
router.register(r'articlecategory', ArticleCategoryViewSet, basename='articlecategory')
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
