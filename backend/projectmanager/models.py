from django.db import models
from django.contrib.auth.models import User

# I believe having blank=True, null=True allows
# http requests to leave them out of the body
# without throwing an error
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
