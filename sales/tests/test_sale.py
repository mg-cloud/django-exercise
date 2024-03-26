"""Test sale."""
import datetime
from decimal import Decimal
from django.utils import timezone
from django.test import RequestFactory, TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from users.models import User
from sales.models import Sale
from sales.serializers import SaleSerializer
from sales.views import SaleViewSet
from .test_article import create_article
from .test_articlecategory import create_category

TEST_SALE_QUANTITY = 10
TEST_SALE_UNIT_SELLING_PRICE = 1100

def create_sale(author, date, article):
    """Create a dummy sale."""
    return Sale.objects.create(date=date, author=author, article=article,
                               quantity=TEST_SALE_QUANTITY, unit_selling_price=TEST_SALE_UNIT_SELLING_PRICE)


class SaleMethodTests(TestCase):
    """Test Sale method."""
    def setUp(self):
        """Set up."""
        self.basic_user1 = User.objects.create_user(email='test1@email.fr')
        self.anewcategory = create_category('anewcategory')
        self.anewarticle = create_article('anewarticle', self.anewcategory)
        self.anewsale = create_sale(self.basic_user1, timezone.now().date(), self.anewarticle)

    def test_total_selling_price(self):
        """Test total selling price."""
        self.assertEqual(self.anewsale.get_total_selling_price(), TEST_SALE_QUANTITY*TEST_SALE_UNIT_SELLING_PRICE)


class SaleTests(TestCase):
    """Test SaleViewSet."""

    def setUp(self):
        """Set up."""
        self.url = reverse_lazy('sale-list')
        self.request = RequestFactory().get(self.url)
        self.basic_user1 = User.objects.create_user(email='test1@email.fr')
        self.basic_user2 = User.objects.create_user(email='test2@email.fr')
        self.anewcategory = create_category('anewcategory1')
        self.anewarticle = create_article('anewarticle1', self.anewcategory)
        self.anewcategory2 = create_category('anewcategory2')
        self.anewarticle2 = create_article('anewarticle2', self.anewcategory2)
        self.sale_data = {
            'date': '2024-01-01',
            'author': reverse('user-detail', kwargs={'pk': self.basic_user1.id}),
            'article': reverse('article-detail', kwargs={'pk': self.anewarticle.id}),
            'quantity': 4,
            'unit_selling_price': 15.0
        }

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
        expected_fields = ['url', 'author', 'date', 'article',
                           'article_category', 'article_code', 'article_name',
                           'quantity', 'unit_selling_price', 'total_selling_price']
        self.assertEqual(list(serialized_sale.get_fields().keys()), expected_fields)

    def test_auth_sorted_sales(self):
        """Test with sales sorted by date."""
        self.request.user = self.basic_user1
        # Add several sales
        for i in range(3):
            create_sale(self.basic_user1, timezone.now().date() + datetime.timedelta(days=i), self.anewarticle)
        for i in range(3):
            create_sale(self.basic_user2, timezone.now().date() + datetime.timedelta(days=i), self.anewarticle)
        # Make sure we get the sales sorted by date
        serialized_sales_list = SaleSerializer(Sale.objects.all().order_by('date').reverse(),
                                               context={'request': self.request},
                                               many=True)
        response = SaleViewSet.as_view({'get': 'list'})(self.request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerySetEqual(response.data['results'], serialized_sales_list.data)

    def test_wo_auth(self):
        """Test without auth and with anonymous user."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.request.user = AnonymousUser()
        response = SaleViewSet.as_view({'get': 'list'})(self.request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_crud_methods(self):
        """Test Create, Update, Delete only by the same user."""
        self.client.force_login(user=self.basic_user1)
        self.assertEqual(Sale.objects.count(), 0)

        # Check create
        response_post = self.client.post(self.url, data=self.sale_data)
        sale_created = response_post.data
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sale.objects.count(), 1)
        # Check total_selling_price
        self.assertEqual(response_post.data['total_selling_price'], 60.0)
        # Check update
        self.sale_data['quantity'] = 1
        response_update_user1 = self.client.put(sale_created['url'],
                                                data=self.sale_data,
                                                content_type='application/json')
        self.assertEqual(response_update_user1.status_code, status.HTTP_200_OK)
        self.assertEqual(Sale.objects.first().quantity, 1)

        # Check update/delete forbidden for a different user
        self.client.force_login(user=self.basic_user2)
        response_update_user2 = self.client.put(sale_created['url'],
                                                data=self.sale_data,
                                                content_type='application/json')
        self.assertEqual(response_update_user2.status_code, status.HTTP_403_FORBIDDEN)
        response_delete_user2 = self.client.delete(sale_created['url'])
        self.assertEqual(response_delete_user2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Sale.objects.count(), 1)

        # Check delete ok with the same user
        self.client.force_login(user=self.basic_user1)
        response_delete_user1 = self.client.delete(sale_created['url'])
        self.assertEqual(response_delete_user1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Sale.objects.count(), 0)

    def test_wrong_sale_update(self):
        self.client.force_login(user=self.basic_user1)
        # Check add wrong quantity
        self.sale_data['quantity'] = -1
        response_post_wrong_quantity = self.client.post(self.url, data=self.sale_data)
        self.assertEqual(response_post_wrong_quantity.status_code, status.HTTP_400_BAD_REQUEST)
        # Check add wrong author
        self.sale_data['author'] = 'test'
        response_post_wrong_author = self.client.post(self.url, data=self.sale_data)
        self.assertEqual(response_post_wrong_author.status_code, status.HTTP_400_BAD_REQUEST)
        # Check add wrong unit selling price
        self.sale_data['unit_selling_price'] = 'test'
        response_post_wrong_unit_selling_price = self.client.post(self.url, data=self.sale_data)
        self.assertEqual(response_post_wrong_unit_selling_price.status_code, status.HTTP_400_BAD_REQUEST)
        # Check add wrong date
        self.sale_data['date'] = '2021-13-32'
        response_post_wrong_date = self.client.post(self.url, data=self.sale_data)
        self.assertEqual(response_post_wrong_date.status_code, status.HTTP_400_BAD_REQUEST)

    def test_aggregated_sales(self):
        """Test aggregated sales view."""
        self.client.force_login(user=self.basic_user1)
        # Check with no sales
        response = self.client.get(reverse('saleaggregated-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerySetEqual(response.data['results'], [])
        # Add a couple of sales for yesterday and today
        today = timezone.now().date()
        yesterday = today - datetime.timedelta(days=1)
        for _ in range(3):
            create_sale(self.basic_user1, yesterday, self.anewarticle)
        # 1 sale today
        create_sale(self.basic_user2, today, self.anewarticle2)
        # 1 sale yesterday
        create_sale(self.basic_user2, today - datetime.timedelta(days=1), self.anewarticle2)
        response = self.client.get(reverse('saleaggregated-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cat1_uri = (self.request.build_absolute_uri(reverse_lazy("articlecategory-detail", args=[self.anewcategory.pk])))
        cat2_uri = (self.request.build_absolute_uri(reverse_lazy("articlecategory-detail", args=[self.anewcategory2.pk])))
        art2_uri = (self.request.build_absolute_uri(reverse_lazy("article-detail", args=[self.anewarticle2.pk])))
        art1_uri = (self.request.build_absolute_uri(reverse_lazy("article-detail", args=[self.anewarticle.pk])))
        # Check the aggregated sales are sorted by sales_total_revenue with the correct last sale date and computed values
        self.assertQuerySetEqual(response.data['results'], [{'article': art1_uri,
                                                             'category': cat1_uri,
                                                             'sales_total_revenue': Decimal('33000'),
                                                             'margin': Decimal('3000.30'),
                                                             'last_sale_date': yesterday},
                                                            {'article': art2_uri,
                                                             'category': cat2_uri,
                                                             'sales_total_revenue': Decimal('22000.00'),
                                                             'margin': Decimal('2000.20'),
                                                             'last_sale_date': today}])
