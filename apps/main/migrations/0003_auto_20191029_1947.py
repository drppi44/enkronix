# Generated by Django 2.2.6 on 2019-10-29 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20191029_1822'),
    ]

    sql = """
    CREATE VIEW main_product_lowest_price_virtual AS
        SELECT main_product.id,
               main_product.name, 
               CAST(MIN(CASE WHEN (main_stockrecord.quantity >= 5 
                 OR main_stockrecord.has_infinite_quantity = True) 
                 THEN main_stockrecord.price ELSE NULL END) AS NUMERIC) AS lowest_price 
        FROM main_product 
        LEFT OUTER JOIN main_stockrecord ON main_product.id = main_stockrecord.product_id
        GROUP BY main_product.id, main_product.name;
    """

    operations = [
        migrations.RunSQL('DROP VIEW IF EXISTS main_product_lowest_price_virtual;'),
        migrations.RunSQL(sql)
    ]

