from django.db import models

class Dealer(models.Model):
    d_id=models.AutoField(primary_key=True)
    dealer_name=models.CharField(max_length=100)
    dealer_address=models.CharField(max_length=300)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0)
    opentime=models.DateTimeField(auto_now_add=False)
    closetime=models.DateTimeField(auto_now_add=False)

    class Meta:
        ordering = ('-d_id',)
        verbose_name_plural = 'Dealers'
        db_table = 'dealer_information'

    def __str__(self):
        return self.dealer_name

