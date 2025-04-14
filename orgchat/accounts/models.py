from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
from organizations.models import Organization
from django.conf import settings

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=50, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects=CustomUserManager()
 
    def __str__(self):
        return self.email


class Role(models.Model):
    POSITION_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='roles'
    )
    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='user'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roles'
    )