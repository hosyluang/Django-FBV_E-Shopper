from django.db import models
from django.conf import settings
from country.models import Category, Brand
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.PositiveIntegerField(default=0, blank=True, null=True)
    company = models.CharField(max_length=200)
    status = models.BooleanField(default=0)
    detail = models.TextField(blank=True, null=True)
    images = models.JSONField(default=list, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
