# Generated by Django 2.1.2 on 2018-10-31 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_auto_20181031_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='c_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
