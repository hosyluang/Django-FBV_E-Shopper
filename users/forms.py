from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=10)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password",
            "confirm_password",
            "avatar",
            "first_name",
            "last_name",
            "id_country",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Username da ton tai.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email da ton tai.")
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            if avatar.size > 1024 * 1024:
                raise ValidationError("Avatar phai nho hon 1MB.")
            if not avatar.name.lower().endswith((".png", ".jpg", ".jpeg")):
                raise ValidationError("Avatar phai co dinh dang png, jpg hoac jpeg.")
        return avatar

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Mat khau xac nhan khong khop.")
        return cleaned_data


class AccountUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "New Password"}),
        required=False,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "avatar",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if self.instance and self.instance.pk:
            if (
                CustomUser.objects.filter(email=email)
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise ValidationError("Email da ton tai.")
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            if avatar.size > 1024 * 1024:
                raise ValidationError("Avatar phai nho hon 1MB.")
            if not avatar.name.lower().endswith((".png", ".jpg", ".jpeg")):
                raise ValidationError("Avatar phai co dinh dang png, jpg hoac jpeg.")
        return avatar

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password or confirm_password:
            if not password:
                raise ValidationError({"password": "Vui long nhap mat khau moi."})
            if not confirm_password:
                raise ValidationError(
                    {"confirm_password": "Vui long xac nhan mat khau."}
                )
            if password != confirm_password:
                raise ValidationError(
                    {"confirm_password": "Mat khau xac nhan khong khop."}
                )
        if not self.has_changed():
            raise ValidationError("Khong co thong tin nao duoc thay doi.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        # Chỉ set password mới nếu người dùng có nhập
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
