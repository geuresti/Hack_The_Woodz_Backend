from django.db import models
from django.contrib.auth.models import User, AbstractUser
                                    # ^should be able to delete

class Project(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    #user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    tools = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title

#class CustomerUser(AbstractUser):

#    name = models.CharField(max_length=25)
#    password = models.CharField(max_length=30)


#    def __str__(self):
#        return name
