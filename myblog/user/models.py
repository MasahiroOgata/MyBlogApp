from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    diary_title = models.CharField(max_length=50, verbose_name='ブログタイトル')
    header_image = models.ImageField(null=True, blank=True)
    title_color = models.CharField(max_length=7, null=True, blank=True)
