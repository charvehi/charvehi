from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
# Create your models here.


class User(AbstractUser):
    #user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_vendor = models.BooleanField('Dealer', default=False)
    city=models.CharField(max_length=100,default='')
    phone_regex = RegexValidator(regex=r'^[6-9]\d{9}$',message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    #phone = models.CharField(max_length=12,default=0)
    #image = models.ImageField(upload_to="profile_pics",null=True,blank=True)

    '''def __str__(self):
        return self.phone'''

'''def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile=UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile,sender=User)'''