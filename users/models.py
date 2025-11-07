from django.db import models
from django.contrib.auth.models import AbstractUser
from country.models import Country
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    id_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null= True, blank=True)

    def __str__(self):
        return self.username
    