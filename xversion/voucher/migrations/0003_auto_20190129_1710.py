# Generated by Django 2.1.2 on 2019-01-29 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0002_remove_coupon_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='image',
            field=models.ImageField(blank=True, db_column='image', null=True, upload_to='voucher/coupons/'),
        ),
    ]
