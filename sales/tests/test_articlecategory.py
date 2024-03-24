"""Test articlecategory."""
from django.test import RequestFactory, TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from users.models import User
from sales.models import ArticleCategory
from sales.serializers import ArticleCategorySerializer
from sales.views import ArticleCategoryViewSet


def create_category(display_name):
    """Create a dummy category."""
    return ArticleCategory.objects.create(display_name=display_name)


class ArticleCategoryViewSetTests(TestCase):
    """Test ArticleCategoryViewSet."""

    def setUp(self):
        """Set up."""
        self.url = reverse_lazy('articlecategory-list')
        self.factory = RequestFactory()
        self.basic_user = User.objects.create_user(email='test1@email.fr')

    def test_auth_no_category(self):
        """Test with no category."""
        self.client.force_login(user=self.basic_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerySetEqual(response.data['results'], [])

    def test_auth_two_category(self):
        """Test with two category correctly serialized."""
        anewcategory1 = create_category('anewcategory1')
        anewcategory2 = create_category('anewcategory2')
        request = self.factory.get(self.url)
        request.user = self.basic_user
        serialized_category1 = ArticleCategorySerializer(anewcategory1, context={'request': request})
        serialized_category2 = ArticleCategorySerializer(anewcategory2, context={'request': request})
        response = ArticleCategoryViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerySetEqual(response.data['results'], [serialized_category1.data, serialized_category2.data])

    def test_wo_auth(self):
        """Test without auth and with anonymous user."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        response = ArticleCategoryViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
