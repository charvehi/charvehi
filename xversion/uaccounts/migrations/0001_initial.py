# Generated by Django 2.1.2 on 2018-11-14 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('uid', models.BigIntegerField(default=0, primary_key=True, serialize=False)),
                ('name', models.CharField(default=0, max_length=60)),
                ('email', models.EmailField(default=0, max_length=254)),
                ('password', models.CharField(default=0, max_length=50)),
                ('mobile', models.CharField(default=0, max_length=10)),
                ('gender', models.CharField(default=0, max_length=1)),
                ('dob', models.CharField(default=0, max_length=11)),
                ('lat', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=9)),
                ('lon', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=9)),
                ('last_login', models.CharField(default=0, max_length=60)),
            ],
            options={
                'db_table': 'uaccounts_userprofileinfo',
            },
        ),
    ]
