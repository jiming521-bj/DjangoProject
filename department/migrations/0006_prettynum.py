# Generated by Django 2.0 on 2023-09-07 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0005_auto_20230907_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrettyNum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=20, verbose_name='手机号')),
                ('price', models.IntegerField(blank=True, default=100, null=True, verbose_name='价格')),
                ('level', models.SmallIntegerField(choices=[(1, '一星'), (2, '二星'), (3, '三星'), (4, '四星'), (5, '五星')], default=1, verbose_name='级别')),
                ('status', models.SmallIntegerField(choices=[(1, '未使用'), (2, '已使用')], default=1, verbose_name='状态')),
            ],
        ),
    ]
