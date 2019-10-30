from django.db import models
from django.db.models import Min, Q, Manager


class LowerPriceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            lowest_price=Min(
                'stock_records__price',
                filter=Q(stock_records__quantity__gte=5) |
                Q(stock_records__has_infinite_quantity=True)
            )
        )


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True)

    objects = LowerPriceManager()


class ProductLowestPriceVirtual(models.Model):
    name = models.CharField(max_length=255, blank=True)
    lowest_price = models.DecimalField(decimal_places=3, max_digits=15)

    class Meta:
        managed = False
        db_table = 'main_product_lowest_price_virtual'


class StockRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='stock_records')
    price = models.DecimalField(decimal_places=3, max_digits=15)

    quantity = models.PositiveIntegerField(default=0)
    has_infinite_quantity = models.BooleanField(default=False)

    on_sale = models.BooleanField(default=False)


class Tag(models.Model):
    name = models.CharField(max_length=25)
    color = models.CharField(max_length=25)


class Order(models.Model):
    status = models.CharField(max_length=12)
    tags = models.ManyToManyField(Tag, blank=True)


