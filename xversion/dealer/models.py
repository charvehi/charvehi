from django.db import models

class Dealer(models.Model):
    d_id = models.AutoField(primary_key=True)
    dealer_name = models.CharField(max_length=100)
    dealer_address = models.CharField(max_length=300)
    dealer_lat = models.DecimalField(max_digits=9, decimal_places=7, blank=True, default=0)
    dealer_lon = models.DecimalField(max_digits=9, decimal_places=7, blank=True, default=0)
    opentime = models.TimeField(auto_now_add=False)
    closetime = models.TimeField(auto_now_add=False)

    class Meta:
        ordering = ('-d_id',)
        verbose_name_plural = 'Dealers'
        db_table = 'dealer_info'

    def __str__(self):
        return self.dealer_name

