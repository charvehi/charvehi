# Generated by Django 2.0.2 on 2019-03-08 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealer',
            name='status',
            field=models.NullBooleanField(default=False, verbose_name='on/off status'),
        ),
    ]