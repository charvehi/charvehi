# Generated by Django 2.1.2 on 2019-01-29 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='expired',
        ),
    ]
