from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save

User = get_user_model()
class Dealer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    d_id = models.AutoField(primary_key=True)
    dealer_name = models.CharField(max_length=100)
    dealer_address = models.CharField(max_length=300)
    dealer_lat = models.DecimalField(max_digits=9, decimal_places=7, blank=True, default=0)
    dealer_lon = models.DecimalField(max_digits=9, decimal_places=7, blank=True, default=0)
    status = models.BooleanField('on/off status',null=True,default=False)
    opentime = models.TimeField(auto_now_add=False,default='20:00')
    closetime = models.TimeField(auto_now_add=False,default='20:00')



    class Meta:
        ordering = ('-d_id',)
        verbose_name_plural = 'Dealers'
        db_table = 'dealer_info'

    def __str__(self):
        return str(self.user)

