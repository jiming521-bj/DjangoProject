# Generated by Django 2.0 on 2023-09-12 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0013_auto_20230910_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='标题')),
                ('detail', models.TextField(verbose_name='详情')),
                ('level', models.SmallIntegerField(choices=[(1, '紧急'), (2, '重要'), (3, '一般'), (4, '延缓')], default=3, verbose_name='级别')),
            ],
        ),
    ]
