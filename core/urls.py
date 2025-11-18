from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("404/", views.four_zero_four, name="four_zero_four"),
    path("contact/", views.contact, name="contact"),
]
