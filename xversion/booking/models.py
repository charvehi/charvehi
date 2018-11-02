from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


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
            return reverse('booking:model_list_by_category', args=[self.slug])


class CategoryModelImage(models.Model):
    img = models.ImageField(upload_to="bike/models/", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Model Images'
        db_table = 'category_model_image'

    def __str__(self):
        return str(self.img)


class CategoryModel(models.Model):   #Model storage table
    m_id = models.AutoField(primary_key=True)
    c_id = models.ForeignKey(Category, null=True, db_column='c_id', on_delete=models.CASCADE)
    #dealer_id=models.ForeignKey()
    model_name = models.CharField(max_length=100)
    price = models.IntegerField()
    model_image = models.ForeignKey(CategoryModelImage, db_column='image', null=True, on_delete=models.CASCADE)
    rating = models.IntegerField()
    status = models.BooleanField(default=False)
    specification = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-created',)
        verbose_name_plural ='Models/Variants'
        db_table = 'category_model'

    def __str__(self):
        return self.model_name

    def get_absolute_url(self):
        return reverse('booking:model_list', args=[self.m_id, self.slug])







