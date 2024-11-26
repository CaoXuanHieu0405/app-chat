from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def set_online(self):
        self.is_online = True
        self.save()

    def set_offline(self):
        self.is_online = False
        self.save()
