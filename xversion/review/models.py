from django.db import models
from django.urls import reverse
from booking.models import CategoryModel


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    model = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.DecimalField(choices=RATING_CHOICES, max_digits=2, decimal_places=1)

    def get_detail_url(self):
        return reverse('review:review_detail', args=[self.id])

    def get_submit_url(self):
        return reverse('review:add_review', args=[self.m_id])
