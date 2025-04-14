from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Role

@receiver(post_save, sender=CustomUser)
def create_user_role(sender, instance, created, **kwargs):
    if created:
        Role.objects.create(
            user=instance,
            position='user',
            organization=None
        )
