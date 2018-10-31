from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Image(models.Model):
    img = models.ImageField(upload_to="bike/category/", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Category Images'
        db_table = 'Image'

    def __str__(self):
        return str(self.img)


class Category(models.Model):
        c_id = models.AutoField(primary_key=True)
        category_name = models.CharField(max_length=60)
        image = models.ForeignKey(Image, db_column='image', null=True, on_delete=models.CASCADE)
        created = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)
        status = models.BooleanField(default=False)

        class Meta:
            ordering = ('-created',)
            verbose_name_plural = 'Category'
            db_table = 'Category'

        def __str__(self):
            return self.category_name

        def get_absolute_url(self):
            return reverse('booking:category_list', args=[self.c_id, self.slug])



