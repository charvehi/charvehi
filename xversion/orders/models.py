from django.db import models
from django.urls import reverse
import datetime
from dateutil.relativedelta import relativedelta


class UserOrderInfo(models.Model):
    x = datetime.datetime.now()
    one = x + relativedelta(days=+0)
    two = x + relativedelta(days=+1)
    three = x + relativedelta(days=+2)
    four = x + relativedelta(days=+3)

    DATE_CHOICES = (
        (1, str(one.day) + " " + str(one.strftime("%b"))),
        (2, str(two.day) + " " + str(two.strftime("%b"))),
        (3, str(three.day) + " " + str(three.strftime("%b"))),
        (4, str(four.day) + " " + str(four.strftime("%b"))),
    )
    uid = models.BigIntegerField(primary_key=True, default=0)
    mid = models.IntegerField(default=0)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0)
    start_date = models.CharField(choices=DATE_CHOICES,blank=False, max_length=6)
    start_time = models.CharField(max_length=8,blank=False)
    end_date = models.CharField(choices=DATE_CHOICES, blank=False, max_length=6)
    end_time = models.CharField(max_length=8,blank=False)

    #REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        verbose_name_plural = 'Orders'
        db_table = 'orders'

    def get_add_url(self):
        return reverse('orders:cart_detail', args=[self.m_id, self.slug])

    def get_remove_url(self):
        return reverse('orders:cart_removes', args=[self.m_id, self.slug])

