from django.urls import path
from . import views

urlpatterns = [
    path("blog-list/", views.blog_list, name="blog_list"),
    path("blog-detail/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("blog-detail/rate/", views.blog_rate, name="blog_rate"),
    path("blog-detail/cmt/", views.blog_cmt, name="blog_cmt"),
    # API
    path("api/list/", views.blog_api_list),
    path("api/create/", views.blog_api_create),
    path("api/detail/<int:pk>/", views.blog_api_detail),
    path("api/update/<int:pk>/", views.blog_api_update),
    path("api/delete/<int:pk>/", views.blog_api_delete),
]
