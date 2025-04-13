from django.db import models
from django.utils import timezone

class Organization(models.Model):
    name = models.CharField(max_length=255)
    detail= models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)