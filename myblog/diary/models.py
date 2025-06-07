from django.db import models
from django.conf import settings
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='タイトル')
    content = models.TextField(max_length=2000, verbose_name='本文')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('diary:detail',
                        kwargs={'username': self.author.username, 'pk': self.pk})
    

