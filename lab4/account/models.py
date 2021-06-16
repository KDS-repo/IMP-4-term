from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

from concurrent.futures import ThreadPoolExecutor

class Profile(models.Model):
    t1 = ThreadPoolExecutor().submit(models.OneToOneField, settings.AUTH_USER_MODEL)
    t2 = ThreadPoolExecutor().submit(models.DateField, blank=True, null=True)
    t3 = ThreadPoolExecutor().submit(models.ImageField, upload_to='users/%Y/%m/%d', blank=True)
    user = t1.result()
    date_of_birth = t2.result()
    photo = t3.result()

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
