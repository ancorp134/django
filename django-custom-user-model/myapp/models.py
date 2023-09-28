from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class CustomUser(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True,default=uuid.uuid1,editable=False)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser,primary_key=True,on_delete=models.CASCADE)
    bio = models.TextField(max_length=50,null=True)
    dob = models.DateField(auto_now_add=False,null=True)
    address = models.CharField(max_length=50,null=True)

    def __str__(self):
        return str(self.user.email)
    
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
