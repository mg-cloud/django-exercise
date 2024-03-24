"""Test article."""
from django.test import RequestFactory, TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from users.models import User
from sales.models import Article
from sales.serializers import ArticleSerializer
from sales.views import ArticleViewSet
from .test_articlecategory import create_category


def create_article(code, category):
    """Create a dummy article."""
    return Article.objects.create(code=code,
                                  category=category,
                                  name='anewarticle',
                                  manufacturing_cost=999.99)


class ArticleTests(TestCase):
    """Test Article."""

    def setUp(self):
        """Set up."""
        self.url = reverse_lazy('article-list')
        self.factory = RequestFactory()
        self.basic_user = User.objects.create_user(email='test1@email.fr', password='astrongpwd')
        self.dummy_category = create_category('anewcatogory')

    def test_auth_no_article(self):
        """Test with no article."""
        self.client.force_login(user=self.basic_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerySetEqual(response.data['results'], [])

    def test_auth_one_article(self):
        """Test with one article correctly serialized."""
        anewarticle = create_article('anewarticle', self.dummy_category)
        request = self.factory.get(self.url)
        request.user = self.basic_user
        serialized_article = ArticleSerializer(anewarticle, context={'request': request})
        response = ArticleViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerySetEqual(response.data['results'], [serialized_article.data])

    def test_wo_auth(self):
        """Test without auth and with anonymous user."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        response = ArticleViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

