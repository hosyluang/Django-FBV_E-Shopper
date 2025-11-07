from django.urls import path
from . import views

urlpatterns = [
    path("my-product/", views.my_product, name="my_product"),
    path("add-product/", views.add_product, name="add_product"),
    path("product-detail/<int:pk>/", views.product_detail, name="product_detail"),
]
