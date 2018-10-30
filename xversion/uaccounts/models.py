from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserProfileInfo(models.Model):
        #user = models.OneToOneField(User, on_delete=models.CASCADE)
        uid =  models.BigIntegerField(primary_key=True, default=0)
        name = models.CharField(max_length=60, default=0)
        email = models.EmailField(default=0, blank=False)
        password = models.CharField(max_length=50, default=0, blank=False)
        #phone_regex = RegexValidator(regex=r'^d{6,10}$', message="Invalid number.")
        mobile = models.CharField(max_length=10, default=0)
        gender = models.CharField(max_length=1, default=0)
        dob = models.CharField(max_length=11, default=0)
        lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0)
        lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0)
        last_login = models.CharField(max_length=60, default=0)

        REQUIRED_FIELDS = ['email', 'password']
        USERNAME_FIELD = 'email'

        class Meta():
                #model = User
                #fields = ('email', 'password')
                db_table = 'uaccounts_userprofileinfo'

def __str__(self):
  return self.user.email