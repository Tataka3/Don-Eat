from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import ProfileModel


CATEGORY_CHOICES = (
    ('VEG','VEG'),
    ('NON VEG','NON VEG'),
)

# Create your models here.
class Item(models.Model):
    posting_organization = models.OneToOneField(ProfileModel,on_delete=models.CASCADE,null=True,related_name = 'posting_organization')
    ordering_organization = models.OneToOneField(ProfileModel,on_delete=models.CASCADE,null=True,related_name = 'ordering_organization')
    isOrdered = models.BooleanField(default=False,null=True)
    isQualityOK = models.BooleanField(default=False,null=True)
    isQuantityOK = models.BooleanField(default=False,null=True)
    description = models.CharField(max_length=100)
    quantity = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES, default='VEG',null=True,max_length=100)
    image = models.ImageField(default='default.png',upload_to='profile_pics')
    freshTill = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.pk} {self.organization}'