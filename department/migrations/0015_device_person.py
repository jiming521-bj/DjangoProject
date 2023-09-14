# Generated by Django 2.0 on 2023-09-12 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0014_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='person',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='department.Admin', verbose_name='负责人'),
        ),
    ]