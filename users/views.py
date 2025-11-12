from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegisterForm


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
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def custom_logout(request):
    logout(request)
    return redirect("login")


@login_required
def account(request):
    user = request.user
    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        if "avatar" in request.FILES:
            user.avatar = request.FILES["avatar"]
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password:
            if password == confirm_password:
                user.set_password(password)
                update_session_auth_hash(request, user)  # giữ đăng nhập
            else:
                messages.error(request, "Cập nhật thất bại, mật khẩu không khớp")
                return redirect("account")
        user.save()
        messages.success(request, "Cập nhật thành công!")
        return redirect("account")
    return render(request, "users/account.html", {"user": user})
