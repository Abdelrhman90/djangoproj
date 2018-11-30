from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):

    user=models.OneToOneField(User)

    Portfolio = models.URLField(blank=True)
    Profile_Pic= models.ImageField(blank=True, upload_to = 'Profile_Pics')
    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username
