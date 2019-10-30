import json

from django.test import TestCase
from rest_framework.reverse import reverse

from apps.main.models import StockRecord, Product, ProductLowestPriceVirtual, Tag, Order


class ProductStockTests(TestCase):
    def setUp(self):
        tomato = Product.objects.create(name='Tomato')
        milk = Product.objects.create(name='Milk')

        StockRecord.objects.bulk_create(
            StockRecord(**params)
            for params in [
                dict(price=10, quantity=2, has_infinite_quantity=False, on_sale=True, product=tomato),
                dict(price=5, quantity=10, has_infinite_quantity=True, on_sale=False, product=tomato),
                dict(price=10, quantity=10, has_infinite_quantity=False, on_sale=True, product=tomato),
                dict(price=8, quantity=2, has_infinite_quantity=True, on_sale=True, product=tomato),
                dict(price=10, quantity=1, has_infinite_quantity=False, on_sale=True, product=milk),
                dict(price=5, quantity=1, has_infinite_quantity=True, on_sale=True, product=milk),
                dict(price=3, quantity=10, has_infinite_quantity=False, on_sale=False, product=milk),
                dict(price=8, quantity=5, has_infinite_quantity=False, on_sale=True, product=milk),
            ]
        )

    def check(self, data):
        self.assertEqual(data[0][0], 'Tomato')
        self.assertEqual(data[0][1], 5)
        self.assertEqual(data[1][0], 'Milk')
        self.assertEqual(data[1][1], 3)

    def test_lowest_price_with_manager(self):
        data = Product.objects.values_list('name', 'lowest_price')
        self.check(data)

    def test_lowest_price_with_table_view(self):
        data = ProductLowestPriceVirtual.objects.values_list('name', 'lowest_price')
        self.check(data)


class OrderTagTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(status='started')
        self.tag1 = Tag.objects.create(name='tag1', color='red')
        self.tag2 = Tag.objects.create(name='tag2', color='blue')
        self.tag3 = Tag.objects.create(name='tag3', color='pink')
        self.order.tags.add(self.tag1)
        self.order.tags.add(self.tag2)

    def test_order_list(self):
        response = self.client.get(reverse('order-list'))
        data = [{'id': self.order.id,
                 'status': self.order.status,
                 'tags_info': [{'id': self.tag1.id, 'name': self.tag1.name, 'color': self.tag1.color},
                               {'id': self.tag2.id, 'name': self.tag2.name, 'color': self.tag2.color}]}]
        self.assertEqual(response.data, data)

    def test_tag_list(self):
        response = self.client.get(reverse('tag-list'))
        self.assertEqual(
            response.data,
            [{'id': self.tag1.id, 'name': self.tag1.name, 'color': self.tag1.color},
             {'id': self.tag2.id, 'name': self.tag2.name, 'color': self.tag2.color},
             {'id': self.tag3.id, 'name': self.tag3.name, 'color': self.tag3.color}])

    def test_create_tag(self):
        tag_json = {'name': 'test-tag', 'color': 'yellow'}
        response = self.client.post(reverse('tag-list'), data=tag_json, format='json')
        tag = Tag.objects.last()
        self.assertEqual(response.data, {'id': tag.id, 'name': tag.name, 'color': tag.color})

    def test_tag_delete(self):
        response = self.client.delete(reverse('tag-detail', kwargs={'pk': self.tag1.id}))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Tag.objects.filter(id=self.tag1.id).exists())

    def test_order_create_with_tag(self):
        order_data = {'status': self.order.status, 'tags': [self.tag1.id, self.tag2.id]}
        response = self.client.post(reverse('order-list'), order_data, format='json')
        data = {'id': response.data['id'],
                'status': self.order.status,
                'tags_info': [{'id': self.tag1.id, 'name': self.tag1.name, 'color': self.tag1.color},
                              {'id': self.tag2.id, 'name': self.tag2.name, 'color': self.tag2.color}]}
        self.assertEqual(response.data, data)

    def test_order_add_tag(self):
        data = {'status': self.order.status, 'tags': [self.tag1.id, self.tag2.id, self.tag3.id]}
        response = self.client.put(reverse('order-detail', kwargs={'pk': self.order.id}),
                                   data=json.dumps(data), content_type='application/json')
        data = {'id': response.data['id'],
                'status': self.order.status,
                'tags_info': [{'id': self.tag1.id, 'name': self.tag1.name, 'color': self.tag1.color},
                              {'id': self.tag2.id, 'name': self.tag2.name, 'color': self.tag2.color},
                              {'id': self.tag3.id, 'name': self.tag3.name, 'color': self.tag3.color}]}
        self.assertEqual(response.data, data)

    def test_order_tag_delete(self):
        data = {'status': self.order.status, 'tags': []}
        response = self.client.put(reverse('order-detail', kwargs={'pk': self.order.id}),
                                   data=json.dumps(data), content_type='application/json')
        data = {'id': response.data['id'],
                'status': self.order.status,
                'tags_info': []}
        self.assertEqual(response.data, data)
