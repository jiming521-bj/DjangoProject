# Generated by Django 4.2.5 on 2023-09-05 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_userinfo_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='data',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
