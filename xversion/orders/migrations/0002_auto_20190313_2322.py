# Generated by Django 2.0.2 on 2019-03-13 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorderinfo',
            name='order_id',
            field=models.BigIntegerField(default=0),
        ),
    ]
