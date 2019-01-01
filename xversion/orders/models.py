from django.db import models
from django.urls import reverse


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

    def get_add_url(self):
        return reverse('orders:cart_detail', args=[self.m_id, self.slug])

    def get_remove_url(self):
        return reverse('orders:cart_removes', args=[self.m_id, self.slug])

