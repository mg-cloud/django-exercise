"""Test sale."""
import datetime
from django.utils import timezone
from django.test import RequestFactory, TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from users.models import User
from sales.models import Sale
from sales.serializers import SaleSerializer
from sales.views import SaleViewSet
from .test_article import create_article
from .test_articlecategory import create_category


def create_sale(author, date, article):
    """Create a dummy sale."""
    return Sale.objects.create(date=date, author=author, article=article, quantity=10, unit_selling_price=9.1)


class SaleModelTests(TestCase):
    """Test SaleModel."""
    def setUp(self):
        """Set up."""
        self.basic_user1 = User.objects.create_user(email='test1@email.fr', password='astrongpwd')
        self.anewcategory = create_category('anewarticle')
        self.anewarticle = create_article('anewarticle', self.anewcategory)
        self.anewsale = create_sale(self.basic_user1, timezone.now().date(), self.anewarticle)

    def test_total_selling_price(self):
        """Test total selling price."""
        self.assertEqual(self.anewsale.get_total_selling_price(), 91.0)


class SaleViewSetTests(TestCase):
    """Test SaleViewSet."""

    def setUp(self):
        """Set up."""
        self.url = reverse_lazy('sale-list')
        self.factory = RequestFactory()
        self.basic_user1 = User.objects.create_user(email='test1@email.fr', password='astrongpwd')
        self.basic_user2 = User.objects.create_user(email='test2@email.fr', password='astrongpwd')
        self.anewcategory = create_category('anewarticle')
        self.anewarticle = create_article('anewarticle', self.anewcategory)

    def test_auth_no_sale(self):
        """Test with no sale."""
        self.client.force_login(user=self.basic_user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerySetEqual(response.data['results'], [])

    def test_serialized_data(self):
        """Test with sale serialized fields."""
        anewsale = create_sale(self.basic_user2, timezone.now().date(), self.anewarticle)
        # Make sure we serialized the expected fields
        serialized_sale = SaleSerializer(anewsale, context={'request': None})
        expected_fields = ['date',
                           'article_category',
                           'article_code',
                           'article_name',
                           'quantity',
                           'unit_selling_price',
                           'total_selling_price']
        self.assertEqual(list(serialized_sale.get_fields().keys()), expected_fields)

        # date, catégorie article, code article, nom article, quantité, prix de vente unitaire, prix de vente total

    def test_auth_sorted_sales(self):
        """Test with sales sorted by date."""
        request = self.factory.get(self.url)
        request.user = self.basic_user1
        # Add several sales
        for i in range(3):
            create_sale(self.basic_user1, timezone.now().date() + datetime.timedelta(days=i), self.anewarticle)
        for i in range(3):
            create_sale(self.basic_user2, timezone.now().date() + datetime.timedelta(days=i), self.anewarticle)
        # Make sure we get the sales sorted by date
        serialized_sales_list = SaleSerializer(Sale.objects.all().order_by('date').reverse(),
                                               context={'request': request},
                                               many=True)
        response = SaleViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerySetEqual(response.data['results'], serialized_sales_list.data)

    def test_wo_auth(self):
        """Test without auth and with anonymous user."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        response = SaleViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
