from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

from concurrent.futures import ThreadPoolExecutor

class Profile(models.Model):
    user = OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
