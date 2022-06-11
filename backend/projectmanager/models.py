from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# I believe having blank=True, null=True allows
# http requests to leave them out of the body
# without throwing an error

# to extend the User model, I created a Profile model as a custom of User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=30, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
class Project(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    long_description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=150, blank=True, null=True)
    contributions = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='images/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title
