from django.db import models

# Create your models here.
class DanggeunPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=200)
    price = models.IntegerField()
    status = models.CharField(max_length=1, default='N')
    views = models.IntegerField(default=0)
    chat = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    author_id = models.CharField(max_length=100, null=True, blank=True)
    post_id = models.CharField(max_length=100, null=True, blank=True)
    trading_location = models.CharField(max_length=100)
    publish = models.CharField(max_length=1, default='Y')