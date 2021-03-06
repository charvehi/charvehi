# Generated by Django 2.0.2 on 2019-03-13 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserOrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.BigIntegerField()),
                ('u_id', models.BigIntegerField(default=0)),
                ('name', models.CharField(default=0, max_length=40)),
                ('mobile', models.IntegerField(default=0)),
                ('d_id', models.IntegerField(default=0)),
                ('m_id', models.IntegerField(default=0)),
                ('booked_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField(max_length=6)),
                ('start_time', models.CharField(max_length=8)),
                ('end_date', models.DateField(max_length=6)),
                ('end_time', models.CharField(max_length=8)),
                ('duration', models.CharField(default=0, max_length=30)),
                ('delivery', models.BooleanField(default=False)),
                ('price_hour', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('price_day', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('dealer_money', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('lat', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=9)),
                ('lon', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=9)),
            ],
            options={
                'verbose_name_plural': 'Orders',
                'db_table': 'orders',
            },
        ),
    ]
