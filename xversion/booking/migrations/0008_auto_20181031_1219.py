# Generated by Django 2.1.2 on 2018-10-31 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_auto_20181031_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ForeignKey(db_column='image', null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.Image'),
        ),
    ]
