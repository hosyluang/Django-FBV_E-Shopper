from django.urls import path
from . import views

urlpatterns = [
    path('blog-list/', views.blog_list, name='blog_list'),
    path('blog-detail/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog-detail/rate/', views.blog_rate, name='blog_rate'),
    path('blog-detail/cmt/', views.blog_cmt, name='blog_cmt'),
]