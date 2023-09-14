# Generated by Django 2.0 on 2023-09-12 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0015_device_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='level',
            field=models.SmallIntegerField(choices=[(1, '紧急'), (2, '重要'), (3, '一般'), (4, '延缓')], verbose_name='级别'),
        ),
    ]