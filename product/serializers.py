from rest_framework import serializers
from .models import Product


class ProductSeializer(serializers.ModelSerializer):
    model = Product
