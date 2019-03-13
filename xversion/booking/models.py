from django.db import models
from django.urls import reverse
from dealer.models import Dealer
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import numpy as np


class Image(models.Model):
    img = models.ImageField(upload_to="bike/category/", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Category Images'
        db_table = 'category_image'

    def __str__(self):
        return str(self.img)


class Category(models.Model):
        c_id = models.AutoField(primary_key=True)
        category_name = models.CharField(max_length=60)
        image = models.ForeignKey(Image, db_column='image', null=True, on_delete=models.CASCADE)
        created = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)
        status = models.BooleanField(default=False)
        slug = models.SlugField(max_length=150, unique=True, db_index=True)

        class Meta:
            ordering = ('-created',)
            verbose_name_plural = 'Category'
            db_table = 'category'

        def __str__(self):
            return self.category_name

        def get_absolute_url(self):
            return reverse('booking:model_list_by_category', args=[self.c_id, self.slug])


class CategoryModelImage(models.Model):
    img = models.ImageField(upload_to="bike/models/", null=True, blank=True)
    img1 = models.ImageField(upload_to="bike/models/", null=True, blank=True)
    img2 = models.ImageField(upload_to="bike/models/", null=True, blank=True)
    img3 = models.ImageField(upload_to="bike/models/", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Model Images'
        db_table = 'category_model_image'

    def __str__(self):
        return str(self.img)


class CategoryModel(models.Model):   #Model storage table
    DAY_COUNT_CHOICES = (
        (1, '12'),
        (2, '24'),
    )

    m_id = models.AutoField(primary_key=True)
    c_id = models.ForeignKey(Category, null=True, db_column='c_id', on_delete=models.CASCADE)
    d_id = models.ForeignKey(Dealer, null=True, db_column='d_id', on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    model_image = models.ForeignKey(CategoryModelImage, db_column='image', null=True, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    specification = models.CharField(max_length=300)

    #------------------for difference calculation-one time (N1) --------------------#
    price_hour_offline = models.DecimalField('Price hour offline (static)', max_digits=6, decimal_places=2, default=0)
    price_day_offline = models.DecimalField('Price day offline (static)', max_digits=6, decimal_places=2, default=0)
    #----------------------------------ends--------------------------------------#

    #----reference for price_hour-----#
    price_hour_dealer = models.DecimalField('Price hour (Dealer)', max_digits=6, decimal_places=2, default=0)
    #----ends-----#

    price_hour = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    ph_count = models.IntegerField(default=0)

    #----reference for price_day-----#
    price_day_dealer = models.DecimalField('Price day (Dealer)', max_digits=6, decimal_places=2, default=0)
    #----ends-----#

    price_day = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    pd_count = models.IntegerField(choices=DAY_COUNT_CHOICES, default=0)

    is_delivery = models.BooleanField('Delivery', default=False)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
        return np.mean(all_ratings)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.model_name

    class Meta:
        ordering = ('-created',)
        verbose_name_plural ='Models/Variants'
        db_table = 'category_model'

    def get_absolute_url(self):
        return reverse('booking:category_model_details', args=[self.m_id, self.slug])

    def get_detail_url(self):
        return reverse('booking:category_model_details', args=[self.m_id, self.slug])

    def get_order_url(self):
        return reverse('orders:cart_add', args=[self.m_id, self.slug])







