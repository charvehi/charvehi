# Generated by Django 2.1.2 on 2019-01-18 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('user_name', models.CharField(max_length=100)),
                ('comment', models.CharField(max_length=200)),
                ('rating', models.DecimalField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], decimal_places=1, max_digits=2)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.CategoryModel')),
            ],
        ),
    ]
