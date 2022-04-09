from django.db import models
from django.contrib.auth.models import User



ORG_CHOICES = (
    ('Individual','Individual'),
    ('NGO','NGO'),
    ('Private', 'Private'),
    ('Residential','Residential'),
    ('Event','Event'),
    ('Others','Others'),
)

CATEGORY_CHOICES = (
    ('USER','USER'),
    ('DELIVERY','DELIVERY'),
)

# Create your models here.
class ProfileModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY_CHOICES, default='USER',null=True,max_length=100)
    image = models.ImageField(default='default.png',upload_to='profile_pics')
    instituteName = models.CharField(max_length=100,null=True)
    instituteType = models.CharField(choices=ORG_CHOICES, default='Others',null=True,max_length=100)
    location = models.CharField(max_length=100,null=True)
    acceptanceRate = models.FloatField(null=True,default=0)
    walletPublicAddress = models.CharField(max_length=50,null=True,default=0)

    def __str__(self):
        return f'{self.user.username} {self.category} profile'


