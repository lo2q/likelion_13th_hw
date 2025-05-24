from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model) :
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     birth = models.DateField(null=True, blank=True) 
     phone_number = models.CharField(max_length=15, null=True, blank=True)
     bio = models.TextField(null=True, blank=True)
     followings = models.ManyToManyField("self", related_name="followers", symmetrical=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
     if created:
          Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
     instance.profile.save()