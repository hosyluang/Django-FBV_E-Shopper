from django_shop.decorators import non_superuser_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, logout, authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer
from django.contrib import messages
from .forms import RegisterForm, AccountUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_superuser = False
            user.is_staff = False
            user.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff or user.is_superuser:
                return redirect("login")
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def custom_logout(request):
    logout(request)
    return redirect("login")


@non_superuser_required
def account(request):
    if request.method == "POST":
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get("password"):
                update_session_auth_hash(request, user)
            messages.success(request, "Cap nhat thong tin thanh cong")
            return redirect("account")
        else:
            messages.error(request, "Cap nhat that bai")
    else:
        form = AccountUpdateForm(instance=request.user)
    return render(request, "users/account.html", {"form": form})


# API
@api_view(["GET"])
def user_api_list(request):
    user = CustomUser.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def user_api_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        password = serializer.validated_data.pop("password")
        user = serializer.save()
        user.set_password(password)
        user.is_active = True
        user.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def user_api_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # neu dung thi login thanh cong va tao ss
            return Response(
                {"message": "Login thanh cong", "user_id": user.id},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Tai khoan hoac mat khau sai"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return Response()


@api_view(["PATCH"])
def user_api_update(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid(raise_exception=True):
        password = serializer.validated_data.pop("password")
        user = serializer.save()
        user.set_password(password)
        user.is_active = True
        user.save()
    return Response(serializer.data)


@api_view(["DELETE"])
def user_api_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def user_api_logout(request):
    logout(request)
    return Response({"message": "Logout thanh cong"}, status=status.HTTP_200_OK)
