# Generated by Django 2.1.2 on 2019-01-29 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymodel',
            name='pd_count',
            field=models.IntegerField(choices=[(1, '12'), (2, '24')], default=0),
        ),
    ]
