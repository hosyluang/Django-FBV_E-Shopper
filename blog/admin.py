from django.contrib import admin
from .models import Blog, Rate, Comment

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author', 'created_at')
    list_filter = ['author', 'created_at']
    search_fields = ['title']

class RateAdmin(admin.ModelAdmin):
    list_display = ('id', 'rate', 'id_user', 'id_blog', 'created_at')
    list_filter = ['created_at']

class CmtAdmin(admin.ModelAdmin):
    list_display = ('id', 'cmt', 'get_user_id', 'id_blog', 'level', 'name_user', 'created_at')
    list_filter = ['created_at']
    def get_user_id(self, obj):
        return obj.id_user.id 
    get_user_id.short_description = 'ID User'

admin.site.register(Blog, BlogAdmin)
admin.site.register(Rate, RateAdmin)
admin.site.register(Comment, CmtAdmin)