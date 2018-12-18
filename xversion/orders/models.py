from django.db import models

class UserOrderInfo(models.Model):
    uid = models.BigIntegerField(primary_key=True, default=0)
    mid = models.IntegerField(default=0)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now=True)

    #REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        verbose_name_plural = 'Orders'
        db_table = 'orders'