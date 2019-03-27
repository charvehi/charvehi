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
    order_id = models.CharField(max_length=80, blank=False)
    u_id = models.BigIntegerField(default=0, blank=True)
    name = models.CharField(max_length=40, blank=False, default=0)
    mobile = models.BigIntegerField(default=0)
    d_id = models.IntegerField(default=0)
    m_id = models.IntegerField(default=0)
    booked_at = models.DateTimeField(auto_now=True)
    #start_date = models.CharField(choices=DATE_CHOICES, blank=False, max_length=6)
    start_date = models.DateField(blank=False, max_length=6)
    start_time = models.CharField(max_length=8, blank=False)
    #end_date = models.CharField(choices=DATE_CHOICES, blank=False, max_length=6)
    end_date = models.DateField(blank=False, max_length=6)
    end_time = models.CharField(max_length=8, blank=False)
    duration = models.CharField(max_length=30, blank=False, default=0)
    delivery = models.BooleanField(default=False)
    price_hour = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    price_day = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    dealer_money = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0)
    due = models.BooleanField(default=True)
    #REQUIRED_FIELDS = ['email', 'password']

    def __str__(self):
        template = 'Order Id: {0.order_id}, Dealer Id: {0.d_id}'
        return template.format(self)

    class Meta:
        verbose_name_plural = 'Orders'
        db_table = 'orders'

    def get_add_url(self):
        return reverse('orders:cart_detail', args=[self.m_id, self.slug])

    def get_remove_url(self):
        return reverse('orders:cart_removes', args=[self.m_id, self.slug])

