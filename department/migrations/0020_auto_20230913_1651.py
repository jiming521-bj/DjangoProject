# Generated by Django 2.0 on 2023-09-13 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0019_auto_20230913_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_price',
            field=models.IntegerField(verbose_name='订单价格'),
        ),
    ]