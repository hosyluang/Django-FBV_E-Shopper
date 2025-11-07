from django.contrib import admin
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'avatar', 'first_name', 'last_name', 'id_country')
    list_filter = ['username', 'id_country']
    search_fields = ['username']

# Register your models here.
admin.site.register(CustomUser, UserAdmin)