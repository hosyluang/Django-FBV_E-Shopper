from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.custom_logout, name="logout"),
    path("account/", views.account, name="account"),
    # API
    path("api/list/", views.user_api_list),
    path("api/register/", views.user_api_register),
    path("api/login/", views.user_api_login),
    path("api/logout/", views.user_api_logout),
    path("api/update/<int:pk>/", views.user_api_update),
    path("api/delete/<int:pk>/", views.user_api_delete),
]
