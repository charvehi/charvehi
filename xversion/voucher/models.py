from django.db import models


class Coupon(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    coupon_name = models.CharField(max_length=60)
    image = models.ImageField(db_column='image', upload_to="voucher/coupons/", null=True, blank=True)
    discount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.coupon_name
