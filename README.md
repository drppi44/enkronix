## В наличии модель заказа (упрощенная) и view для их вывода. На фронте заказы форматируются
в канбан доску похожую на trello (в колонки по статусу).

Задача от клиента: добавить функционал тегов как в trello.
Подробнее (после обсуждения с командой): от бекенда нужно иметь возможность
1) Создать тег (id, name, color) / удалить тег / отредактировать тег
2) Получить список всех существующих тегов
3) Добавить к заказу теги по их id
(решено передавать с фронта готовый массив айдишников тегов вместо add/remove функционала)
4) При просмотре заказов видеть список их тегов (в виде полных объектов)

```python
from django.db import models
from rest_framework import mixins, serializers, viewsets


class Order(models.Model):
    status = models.CharField(max_length=12)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'status',
        ]


class OrdersView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
```

##### Решение: https://github.com/drppi44/enkronix/blob/master/apps/main/api.py#L8

## В модели StockRecord хранятся данные о цене продукта.
quantity / has_infinite_quantity - позволяет задать кол-во товара на складе.

Задание: средствами ORM для каждого продукта посчитать самую
дешевую доступную цену при условии покупки 5 единиц продукта

Ожидаемый результат

```python
print(products.values_list('name', 'lowest_price'))
>>> [('Milk', Decimal('5.000')), ('Tomato', Decimal('8.000'))]
```


```python
from django.db import models


class StockRecord(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    price = models.DecimalField(decimal_places=3, max_digits=15)

    quantity = models.PositiveIntegerField(default=0)
    has_infinite_quantity = models.BooleanField(default=False)

    on_sale = models.BooleanField(default=False)


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True)


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

required_quantity = 5
```

##### Решение 1 (через tableview): https://github.com/drppi44/enkronix/blob/master/apps/main/migrations/0003_auto_20191029_1947.py#L12 https://github.com/drppi44/enkronix/blob/master/apps/main/models.py#L22

##### Решение 2 (через model manager): https://github.com/drppi44/enkronix/blob/master/apps/main/models.py#L5
