# Generated by Django 2.0.2 on 2019-03-13 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20190314_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorderinfo',
            name='order_id',
            field=models.CharField(max_length=80),
        ),
    ]
