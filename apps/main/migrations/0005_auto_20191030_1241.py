# Generated by Django 2.2.6 on 2019-10-30 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_order_productlowestpricevirtual_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tags',
            field=models.ManyToManyField(blank=True, to='main.Tag'),
        ),
    ]
