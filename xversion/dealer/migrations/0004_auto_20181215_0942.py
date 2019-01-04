# Generated by Django 2.1.2 on 2018-12-15 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealer', '0003_auto_20181104_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealer',
            name='dealer_lat',
            field=models.DecimalField(blank=True, decimal_places=7, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='dealer_lon',
            field=models.DecimalField(blank=True, decimal_places=7, default=0, max_digits=9),
        ),
    ]